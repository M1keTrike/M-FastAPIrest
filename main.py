from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import user_router, category_router, activity_router, remainder_router
from fastapi.middleware.cors import CORSMiddleware

# Crear la instancia de FastAPI
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(user_router.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(category_router.router, prefix="/categorias", tags=["Categorias"])
app.include_router(activity_router.router, prefix="/actividades", tags=["Actividades"])
app.include_router(remainder_router.router, prefix="/recordatorios", tags=["Recordatorios"])
