from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="FiltroFácil")

@app.get("/")
async def read_root():
    return HTMLResponse("""
    <h1>FiltroFácil</h1>
    <p>¡La aplicación está funcionando!</p>
    <p>Versión de prueba en producción.</p>
    """)

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "Backend funcionando"}