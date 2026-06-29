"""
Servicio de notificaciones y mensajes
---------------------------------------------------
Gestiona mensajes flash y notificaciones para el usuario.
"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from enum import Enum


class TipoNotificacion(str, Enum):
    EXITO = "success"
    ERROR = "error"
    ADVERTENCIA = "warning"
    INFO = "info"


class Notificacion:
    """Clase para representar una notificación"""
    def __init__(self, mensaje: str, tipo: TipoNotificacion = TipoNotificacion.INFO, titulo: str = None):
        self.mensaje = mensaje
        self.tipo = tipo
        self.titulo = titulo
        self.creada_en = datetime.utcnow()
        self.id = str(datetime.utcnow().timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "mensaje": self.mensaje,
            "tipo": self.tipo.value,
            "titulo": self.titulo,
            "creada_en": self.creada_en.isoformat(),
        }


class NotificacionService:
    """Servicio para gestionar notificaciones"""
    
    # Almacenamiento en memoria (en producción usar Redis)
    _notificaciones = {}
    
    @staticmethod
    def crear_notificacion(usuario_id: int, mensaje: str, tipo: TipoNotificacion, titulo: str = None) -> Notificacion:
        """Crea una notificación para un usuario"""
        notif = Notificacion(mensaje, tipo, titulo)
        
        if usuario_id not in NotificacionService._notificaciones:
            NotificacionService._notificaciones[usuario_id] = []
        
        NotificacionService._notificaciones[usuario_id].append(notif)
        
        # Limpiar notificaciones antiguas (más de 1 hora)
        NotificacionService._limpiar_notificaciones_antiguas(usuario_id)
        
        return notif
    
    @staticmethod
    def obtener_notificaciones(usuario_id: int) -> list:
        """Obtiene todas las notificaciones de un usuario"""
        if usuario_id not in NotificacionService._notificaciones:
            return []
        
        return NotificacionService._notificaciones[usuario_id]
    
    @staticmethod
    def obtener_y_limpiar(usuario_id: int) -> list:
        """Obtiene las notificaciones y las elimina"""
        notificaciones = NotificacionService.obtener_notificaciones(usuario_id)
        if usuario_id in NotificacionService._notificaciones:
            del NotificacionService._notificaciones[usuario_id]
        return notificaciones
    
    @staticmethod
    def _limpiar_notificaciones_antiguas(usuario_id: int):
        """Elimina notificaciones más antiguas de 1 hora"""
        if usuario_id not in NotificacionService._notificaciones:
            return
        
        ahora = datetime.utcnow()
        limite = ahora - timedelta(hours=1)
        
        NotificacionService._notificaciones[usuario_id] = [
            notif for notif in NotificacionService._notificaciones[usuario_id]
            if notif.creada_en > limite
        ]
