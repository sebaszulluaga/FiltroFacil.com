from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="FiltroFácil")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <h1>FiltroFácil</h1>
    <p>¡La aplicación está funcionando correctamente!</p>
    <p><a href="/api/models">Ver modelos disponibles</a></p>
    """

@app.get("/api/health")
async def health():
    return {"status": "ok"}