from fastapi import APIRouter, HTTPException
from typing import Dict
from pydantic import BaseModel
from ..services.therapeutic_agent import TherapeuticAgent

router = APIRouter()
agent = TherapeuticAgent()

class AgentChatRequest(BaseModel):
    message: str
    emotion_data: Dict
    therapist_id: str
    patient_id: str

@router.post("/chat")
async def analyze_patient_data(request: AgentChatRequest) -> Dict:
    """
    Analiza los datos emocionales de un paciente específico y genera recomendaciones personalizadas, considerando el mensaje del usuario.
    """
    try:
        emotion_data = request.emotion_data
        if not all(key in emotion_data for key in ['timeline', 'emotion_summary']):
            raise HTTPException(
                status_code=400,
                detail="Datos emocionales incompletos. Se requiere 'timeline' y 'emotion_summary'"
            )
        # Pasar el mensaje del usuario a la lógica del agente
        recommendations = await agent.generate_recommendations(
            patient_id=request.patient_id,
            therapist_id=request.therapist_id,
            emotion_data=emotion_data,
            user_message=request.message
        )
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar recomendaciones: {str(e)}"
        )

@router.get("/health")
async def health_check() -> Dict:
    """
    Verifica el estado del agente terapéutico.
    """
    return {
        "status": "healthy",
        "service": "therapeutic_agent",
        "version": "1.0.0"
    } 