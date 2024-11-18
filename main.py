from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.routers import (
    usuario_router,
    familia_router,
    evento_router,
    actividad_router,
    recordatorio_router,
    notificacion_router,
    pertenece_router,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(usuario_router.router,
                   prefix="/usuarios", tags=["Usuarios"])
app.include_router(familia_router.router,
                   prefix="/familias", tags=["Familias"])
app.include_router(evento_router.router, prefix="/eventos", tags=["Eventos"])
app.include_router(actividad_router.router,
                   prefix="/actividades", tags=["Actividades"])
app.include_router(recordatorio_router.router,
                   prefix="/recordatorios", tags=["Recordatorios"])
app.include_router(notificacion_router.router,
                   prefix="/notificaciones", tags=["Notificaciones"])
app.include_router(pertenece_router.router,
                   prefix="/pertenece", tags=["Pertenece"])
