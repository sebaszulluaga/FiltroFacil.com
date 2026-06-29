from dotenv import load_dotenv

# CRÍTICO: Cargar .env ANTES de cualquier import del backend
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
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

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Sirve la interfaz principal."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    """Sirve la página acerca de."""
    return templates.TemplateResponse("about.html", {"request": request})