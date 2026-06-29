"""
Servicio de estadísticas para el dashboard
---------------------------------------------------
Proporciona métricas agregadas de ventas, ofertas y juegos.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Oferta, Juego, Tienda


class StatsService:
    def __init__(self, db: Session):
        self.db = db

    def obtener_metricas_generales(self):
        """Retorna métricas principales del dashboard"""
        total_juegos = self.db.query(func.count(Juego.id)).scalar() or 0
        total_tiendas = self.db.query(func.count(Tienda.id)).scalar() or 0
        total_ofertas_activas = self.db.query(func.count(Oferta.id)).filter(
            Oferta.activa == True
        ).scalar() or 0
        
        # Ahorro total (suma de diferencias entre precio normal y oferta)
        ahorro_total_result = self.db.query(
            func.sum(Oferta.precio_normal - Oferta.precio_oferta)
        ).filter(Oferta.activa == True).scalar()
        ahorro_total = float(ahorro_total_result) if ahorro_total_result else 0.0
        
        return {
            "total_juegos": total_juegos,
            "total_tiendas": total_tiendas,
            "total_ofertas_activas": total_ofertas_activas,
            "ahorro_total": round(ahorro_total, 2),
        }

    def obtener_juegos_mas_vendidos(self, limite: int = 5):
        """Retorna los juegos con más ofertas activas"""
        juegos = self.db.query(
            Juego,
            func.count(Oferta.id).label("cantidad_ofertas")
        ).outerjoin(Oferta).filter(
            Oferta.activa == True
        ).group_by(Juego.id).order_by(
            func.count(Oferta.id).desc()
        ).limit(limite).all()
        
        resultado = []
        for juego, cantidad in juegos:
            # Obtener descuento promedio para este juego
            desc_promedio = self.db.query(
                func.avg(Oferta.porcentaje_descuento)
            ).filter(
                Oferta.juego_id == juego.id,
                Oferta.activa == True
            ).scalar() or 0
            
            resultado.append({
                "juego": juego,
                "cantidad_ofertas": cantidad,
                "descuento_promedio": round(float(desc_promedio), 1),
            })
        return resultado

    def obtener_tiendas_mas_ofertas(self, limite: int = 5):
        """Retorna las tiendas con más ofertas activas"""
        tiendas = self.db.query(
            Tienda,
            func.count(Oferta.id).label("cantidad_ofertas")
        ).outerjoin(Oferta).filter(
            Oferta.activa == True
        ).group_by(Tienda.id).order_by(
            func.count(Oferta.id).desc()
        ).limit(limite).all()
        
        return [
            {
                "tienda": tienda,
                "cantidad_ofertas": cantidad,
            }
            for tienda, cantidad in tiendas
        ]

    def obtener_distribucion_descuentos(self):
        """Retorna la distribución de ofertas por rango de descuento"""
        rangos = [
            (0, 10, "0-10%"),
            (10, 25, "10-25%"),
            (25, 50, "25-50%"),
            (50, 75, "50-75%"),
            (75, 100, "75-100%"),
        ]
        
        resultado = []
        for min_desc, max_desc, label in rangos:
            cantidad = self.db.query(func.count(Oferta.id)).filter(
                Oferta.porcentaje_descuento >= min_desc,
                Oferta.porcentaje_descuento < max_desc,
                Oferta.activa == True
            ).scalar() or 0
            resultado.append({"rango": label, "cantidad": cantidad})
        
        return resultado

    def obtener_vista_base_datos(self, limite: int = 5):
        """Retorna un resumen visual de las tablas y sus registros recientes"""
        resumen_tablas = {
            "tiendas": self.db.query(func.count(Tienda.id)).scalar() or 0,
            "juegos": self.db.query(func.count(Juego.id)).scalar() or 0,
            "ofertas": self.db.query(func.count(Oferta.id)).scalar() or 0,
        }

        tiendas_recientes = self.db.query(Tienda).order_by(Tienda.id.desc()).limit(limite).all()
        juegos_recientes = self.db.query(Juego).order_by(Juego.id.desc()).limit(limite).all()
        ofertas_recientes = self.db.query(Oferta).order_by(Oferta.actualizada_en.desc(), Oferta.id.desc()).limit(limite).all()

        return {
            "resumen_tablas": resumen_tablas,
            "tiendas_recientes": tiendas_recientes,
            "juegos_recientes": juegos_recientes,
            "ofertas_recientes": ofertas_recientes,
        }
