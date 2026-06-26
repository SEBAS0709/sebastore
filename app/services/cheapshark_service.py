
import httpx
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.models import Tienda, Juego, Oferta
from app.repositories.tienda_repository import TiendaRepository
from app.repositories.juego_repository import JuegoRepository
from app.repositories.oferta_repository import OfertaRepository

CHEAPSHARK_BASE_URL = "https://www.cheapshark.com/api/1.0"
HEADERS = {"User-Agent": "ProyectoExamenWebDeals/1.0 (uso educativo)"}


class CheapSharkSyncService:
    def __init__(self, db: Session):
        self.db = db
        self.tienda_repo = TiendaRepository(db)
        self.juego_repo = JuegoRepository(db)
        self.oferta_repo = OfertaRepository(db)

    def sincronizar_tiendas(self, client: httpx.Client) -> int:
        resp = client.get(f"{CHEAPSHARK_BASE_URL}/stores", headers=HEADERS)
        resp.raise_for_status()
        tiendas_api = resp.json()

        contador = 0
        for t in tiendas_api:
            if t.get("isActive") != 1:
                continue
            cs_id = str(t["storeID"])
            existente = self.tienda_repo.obtener_por_cheapshark_id(cs_id)
            logo = t.get("images", {}).get("logo")
            if existente:
                existente.nombre = t.get("storeName", existente.nombre)
                existente.logo_url = logo
                self.db.commit()
            else:
                self.tienda_repo.crear(
                    Tienda(
                        cheapshark_store_id=cs_id,
                        nombre=t.get("storeName", f"Tienda {cs_id}"),
                        logo_url=logo,
                        activa=True,
                    )
                )
            contador += 1
        return contador

    def sincronizar_ofertas(
        self, client: httpx.Client, paginas: int = 2, page_size: int = 60
    ) -> dict:
        """
        Descarga las mejores ofertas actuales desde CheapShark y las guarda.
        paginas * page_size = cantidad aproximada de ofertas a importar.
        """
        nuevos_juegos = 0
        nuevas_ofertas = 0
        ofertas_actualizadas = 0

        for pagina in range(paginas):
            params = {
                "pageSize": page_size,
                "pageNumber": pagina,
                "sortBy": "Savings",
                "desc": 1,
                "onSale": 1,
            }
            resp = client.get(
                f"{CHEAPSHARK_BASE_URL}/deals", params=params, headers=HEADERS
            )
            resp.raise_for_status()
            ofertas_api = resp.json()
            if not ofertas_api:
                break

            for d in ofertas_api:
                tienda = self.tienda_repo.obtener_por_cheapshark_id(str(d["storeID"]))
                if not tienda:
                    # si la tienda no estaba sincronizada, la creamos al vuelo
                    tienda = self.tienda_repo.crear(
                        Tienda(
                            cheapshark_store_id=str(d["storeID"]),
                            nombre=f"Tienda {d['storeID']}",
                            activa=True,
                        )
                    )

                juego = self.juego_repo.obtener_por_cheapshark_id(d["gameID"])
                if not juego:
                    juego = self.juego_repo.crear(
                        Juego(
                            cheapshark_game_id=d["gameID"],
                            titulo=d.get("title", "Sin título"),
                            imagen_url=d.get("thumb"),
                            metacritic_score=(
                                int(d["metacriticScore"])
                                if str(d.get("metacriticScore", "")).isdigit()
                                else None
                            ),
                        )
                    )
                    nuevos_juegos += 1

                try:
                    precio_normal = float(d.get("normalPrice", 0))
                    precio_oferta = float(d.get("salePrice", 0))
                    descuento = float(d.get("savings", 0))
                    rating = (
                        float(d["dealRating"]) if d.get("dealRating") else None
                    )
                except (TypeError, ValueError):
                    continue

                existente = self.oferta_repo.obtener_por_juego_y_tienda(
                    juego.id, tienda.id
                )
                if existente:
                    self.oferta_repo.actualizar(
                        existente,
                        {
                            "precio_normal": precio_normal,
                            "precio_oferta": precio_oferta,
                            "porcentaje_descuento": descuento,
                            "calificacion_oferta": rating,
                            "url_oferta": f"https://www.cheapshark.com/redirect?dealID={d.get('dealID')}",
                            "activa": True,
                            "actualizada_en": datetime.utcnow(),
                        },
                    )
                    ofertas_actualizadas += 1
                else:
                    self.oferta_repo.crear(
                        Oferta(
                            juego_id=juego.id,
                            tienda_id=tienda.id,
                            precio_normal=precio_normal,
                            precio_oferta=precio_oferta,
                            porcentaje_descuento=descuento,
                            calificacion_oferta=rating,
                            url_oferta=f"https://www.cheapshark.com/redirect?dealID={d.get('dealID')}",
                            activa=True,
                        )
                    )
                    nuevas_ofertas += 1

        return {
            "juegos_nuevos": nuevos_juegos,
            "ofertas_nuevas": nuevas_ofertas,
            "ofertas_actualizadas": ofertas_actualizadas,
        }

    def ejecutar_sincronizacion_completa(self, paginas: int = 2) -> dict:
        with httpx.Client(timeout=20.0) as client:
            total_tiendas = self.sincronizar_tiendas(client)
            resultado_ofertas = self.sincronizar_ofertas(client, paginas=paginas)
        return {"tiendas_sincronizadas": total_tiendas, **resultado_ofertas}
