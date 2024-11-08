from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import usuario_router, familia_router, evento_router, actividad_router, recordatorio_router, notificacion_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(usuario_router.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(familia_router.router, prefix="/familias", tags=["Familias"])
app.include_router(evento_router.router, prefix="/eventos", tags=["Eventos"])
app.include_router(actividad_router.router, prefix="/actividades", tags=["Actividades"])
app.include_router(recordatorio_router.router, prefix="/recordatorios", tags=["Recordatorios"])
app.include_router(notificacion_router.router, prefix="/notificaciones", tags=["Notificaciones"])
