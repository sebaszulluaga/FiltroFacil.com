from pydantic import BaseModel, Field
from typing import Optional


class RiskLevel(str):
    SAFE = "low"
    SUSPICIOUS = "medium"
    DANGER = "high"


class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Texto o contenido a analizar")


class AnalysisResponse(BaseModel):
    risk_level: str = Field(..., description="Nivel de riesgo: low, medium, o high")
    title: str = Field(..., description="Título simple y llamativo")
    explanation: str = Field(..., description="Explicación con analogía para humanos")
    tips: list[str] = Field(..., description="Lista de consejos de seguridad")
    confidence: Optional[float] = Field(default=None, ge=0.0, le=100.0, description="Porcentaje de confianza")