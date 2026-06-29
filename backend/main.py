from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

# Manteniendo tu router de la API
from backend.api.routes import router

app = FastAPI(
    title="FiltroFácil API",
    description="Servicio de detección de phishing explicada para humanos",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

# Configuración de archivos estáticos y templates con rutas absolutas independientes
BASE_DIR = Path(__file__).resolve().parent.parent

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "frontend" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "frontend" / "templates"))


# CORRECCIÓN DE RUTAS: Sintaxis moderna para Jinja2 en FastAPI
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Pasamos 'request' como argumento de palabra clave y el contexto aparte si fuera necesario
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={}  # Puedes añadir variables aquí dentro si las necesitas
    )


@app.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    # Corregido el error posicional que rompía Render
    return templates.TemplateResponse(
        request=request, 
        name="about.html", 
        context={}
    )