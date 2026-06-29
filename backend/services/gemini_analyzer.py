import os
import json
import base64
import io
from groq import Groq
from PIL import Image
from backend.models.analysis import AnalysisResponse

SYSTEM_PROMPT = """Eres un analista senior en ciberseguridad especializado en detección de phishing. Analiza el contenido y determina si representa un riesgo de fraude o estafa.

MÉTODO DE ANÁLISIS:
1. Identifica señales rojas: urgencia ("¡Urgente!", "24 horas"), amenazas ("bloquearé tu cuenta"), solicitud de credenciales, URLs sospechosas, errores gramaticales, dominios extraños
2. Evalúa tono persuasivo y lenguaje de manipulación emocional
3. Detecta inconsistencias: promesas que parecen demasiado buenas, solicitudes imposibles, remitentes falsos

RESPUESTA EN JSON ESTRICTO:
{
  "risk_level": "high/medium/low",
  "title": "Título claro y profesional",
  "explanation": "Explicación de 2-3 líneas identificando señales de alerta específicas. Lenguaje claro para usuarios no técnicos pero preciso para expertos.",
  "tips": ["Paso 1: verificar remitente en contactos oficiales", "Paso 2: no hacer clic en enlaces sospechosos", "Paso 3: reportar a IT/security si es corporativo"],
  "confidence": 85.0
}

CONSEJOS ACCIONABLES:
- Siempre verifica remitente oficial
- No descargues archivos adjuntos inesperados  
- Busca el dominio oficial directamente (no hagas clic)
- Reporta correos sospechosos a tu equipo de seguridad"""

VISION_MODELS = [
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "qwen/qwen3.6-27b"
]


def _get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY no está configurada")
    return Groq(api_key=api_key)


def parse_response(response_text: str) -> AnalysisResponse:
    try:
        json_text = response_text.strip()
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0]
        elif "```" in json_text:
            json_text = json_text.split("```")[1].split("```")[0]
        
        data = json.loads(json_text)
        return AnalysisResponse(
            risk_level=data.get("risk_level", "low"),
            title=data.get("title", "Análisis completado"),
            explanation=data.get("explanation", ""),
            tips=data.get("tips", []),
            confidence=data.get("confidence", 85.0)
        )
    except Exception:
        return AnalysisResponse(
            risk_level="low",
            title="Error en el análisis",
            explanation="No pudimos analizar el contenido. Inténtalo de nuevo.",
            tips=["Mantén tus datos seguros"],
            confidence=85.0
        )


def analyze_text(text: str) -> AnalysisResponse:
    client = _get_client()
    prompt = f"{SYSTEM_PROMPT}\n\nTexto a analizar:\n{text}"
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1000
    )
    return parse_response(response.choices[0].message.content)


def analyze_image(image_bytes: bytes, mime_type: str) -> AnalysisResponse:
    client = _get_client()
    prompt = f"{SYSTEM_PROMPT}\n\nAnaliza esta captura de pantalla. Primero extrae el texto visible (OCR), luego evalúa si es phishing."
    
    # Redimensionar imagen para reducir tokens
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    max_width = 800
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)
    
    # Convertir a JPEG con calidad reducida
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=80)
    compressed_bytes = buffer.getvalue()
    
    image_base64 = base64.b64encode(compressed_bytes).decode('utf-8')
    clean_base64 = image_base64.replace("\n", "").replace("\r", "").strip()
    
    # Intentar con modelos de visión (fallback)
    last_error = None
    for model in VISION_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{clean_base64}"}}
                    ]
                }],
                temperature=0.2,
                max_tokens=500
            )
            return parse_response(response.choices[0].message.content)
        except Exception as e:
            last_error = str(e)
            continue
    
    # Si todos fallan, devolver error claro
    raise ValueError(f"Todos los modelos de visión fallaron. Último error: {last_error}")


def is_gemini_available() -> bool:
    return bool(os.getenv("GROQ_API_KEY"))