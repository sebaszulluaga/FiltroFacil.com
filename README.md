# FiltroFácil

Aplicación web para detección de phishing con IA (Gemini 2.5 Flash) e interfaz amigable para usuarios no técnicos.

## Configuración

1. Crear archivo `.env` en la raíz:
```bash
GEMINI_API_KEY=tu_api_key_de_google_ai_studio
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn backend.main:app --reload
```

## API Endpoints

- `GET /api/health` - Estado del servicio y Gemini
- `POST /api/analyze` - Analizar texto (JSON: `{"text": "..."}`)
- `POST /api/analyze-image` - Analizar imagen (multipart form: `file`)

## Respuesta del análisis

```json
{
  "risk_level": "high|medium|low",
  "title": "Título simple",
  "explanation": "Explicación con analogía",
  "tips": ["Consejo 1", "Consejo 2"],
  "confidence": 85.5
}
```

## Frontend

- Interfaz mobile-first con Tailwind CSS
- Pestañas: Texto o Imagen
- Drag & drop con soporte cámara móvil
- Semáforo visual: 🔴 Rojo (peligro) / 🟡 Amarillo (sospechoso) / 🟢 Verde (seguro)