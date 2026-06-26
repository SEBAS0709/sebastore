
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx

from app.database import get_db
from app.services.cheapshark_service import CheapSharkSyncService

router = APIRouter(prefix="/api/sync", tags=["Sincronización"])


@router.post("/cheapshark")
def sincronizar_con_cheapshark(paginas: int = 2, db: Session = Depends(get_db)):
   
    try:
        resultado = CheapSharkSyncService(db).ejecutar_sincronizacion_completa(
            paginas=paginas
        )
        return {"ok": True, **resultado}
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=502,
            detail=f"No se pudo contactar a CheapShark: {e}",
        )
