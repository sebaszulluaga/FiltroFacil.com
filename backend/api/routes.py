from fastapi import APIRouter, HTTPException, UploadFile, File
from backend.models.analysis import AnalysisRequest, AnalysisResponse
from backend.services.gemini_analyzer import analyze_text, analyze_image, is_gemini_available

router = APIRouter()


@router.get("/health", response_model=dict)
async def health_check():
    """Endpoint de salud para verificar que el servicio está activo."""
    groq_status = "configured" if is_gemini_available() else "missing_api_key"
    return {
        "status": "ok",
        "service": "FiltroFácil API",
        "groq": groq_status
    }


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_text_endpoint(request: AnalysisRequest):
    """Analiza un texto y detecta si es phishing."""
    if not is_gemini_available():
        raise HTTPException(
            status_code=503,
            detail="El servicio de IA no está configurado. Configure GROQ_API_KEY"
        )
    
    try:
        result = analyze_text(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el análisis: {str(e)}")


@router.post("/analyze-image", response_model=AnalysisResponse)
async def analyze_image_endpoint(file: UploadFile = File(...)):
    """Analiza una imagen (screenshot) y detecta phishing."""
    if not is_gemini_available():
        raise HTTPException(
            status_code=503,
            detail="El servicio de IA no está configurado. Configure GROQ_API_KEY"
        )
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser una imagen (jpg, png, webp, etc.)"
        )
    
    try:
        image_bytes = await file.read()
        result = analyze_image(image_bytes, file.content_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el análisis de imagen: {str(e)}")