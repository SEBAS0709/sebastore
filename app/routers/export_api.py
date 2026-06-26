"""
CAPA DE PRESENTACIÓN - Exportación de reportes
"""
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.oferta_repository import OfertaRepository
from app.services import export_service

router = APIRouter(prefix="/api/export", tags=["Reportes"])


@router.get("/csv")
def exportar_csv(db: Session = Depends(get_db)):
    ofertas = OfertaRepository(db).listar(limit=10_000)
    buffer = export_service.exportar_csv(ofertas)
    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ofertas.csv"},
    )


@router.get("/excel")
def exportar_excel(db: Session = Depends(get_db)):
    ofertas = OfertaRepository(db).listar(limit=10_000)
    buffer = export_service.exportar_excel(ofertas)
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=ofertas.xlsx"},
    )


@router.get("/pdf")
def exportar_pdf(db: Session = Depends(get_db)):
    ofertas = OfertaRepository(db).listar(limit=10_000)
    buffer = export_service.exportar_pdf(ofertas)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=ofertas.pdf"},
    )
