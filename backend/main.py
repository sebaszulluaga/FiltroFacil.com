from dotenv import load_dotenv
load_dotenv()  # Cargar variables de entorno primero

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

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

# Configuración de archivos estáticos y templates con rutas absolutas
BASE_DIR = Path(__file__).resolve().parent.parent

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "frontend" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "frontend" / "templates"))


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Sirve la interfaz principal."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    """Sirve la página acerca de."""
    return templates.TemplateResponse("about.html", {"request": request})