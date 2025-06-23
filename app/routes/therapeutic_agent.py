from fastapi import APIRouter, HTTPException
from typing import Dict
from ..services.therapeutic_agent import TherapeuticAgent

router = APIRouter()
agent = TherapeuticAgent()

@router.post("/chat")
async def analyze_patient_data(
    therapist_id: str,
    patient_id: str,
    data: Dict
) -> Dict:
    """
    Analiza los datos emocionales de un paciente específico y genera recomendaciones personalizadas.
    
    Args:
        therapist_id: ID del terapeuta
        patient_id: ID del paciente
        data: Diccionario con los datos emocionales
            {
                "emotion_data": {
                    "timeline": {segundo: emoción},
                    "emotion_summary": {emoción: conteo}
                }
            }
        
    Returns:
        Dict con recomendaciones, análisis y recursos específicos para el paciente
    """
    try:
        # Validar estructura de datos
        if "emotion_data" not in data:
            raise HTTPException(
                status_code=400,
                detail="Se requiere el campo 'emotion_data'"
            )
            
        emotion_data = data["emotion_data"]
        if not all(key in emotion_data for key in ['timeline', 'emotion_summary']):
            raise HTTPException(
                status_code=400,
                detail="Datos emocionales incompletos. Se requiere 'timeline' y 'emotion_summary'"
            )
            
        recommendations = await agent.generate_recommendations(
            patient_id=patient_id,
            therapist_id=therapist_id,
            emotion_data=emotion_data
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
    
    Returns:
        Dict con el estado del servicio
    """
    return {
        "status": "healthy",
        "service": "therapeutic_agent",
        "version": "1.0.0"
    } 