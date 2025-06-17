from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, List
from agent import TherapeuticAgent
import uvicorn
from datetime import datetime

app = FastAPI(title="EmotionAI Therapeutic Agent")
agent = TherapeuticAgent()

@app.get("/")
async def root():
    return {"message": "Agent is running"}

class SessionEmotionData(BaseModel):
    timeline: Dict[str, str]  # timestamp -> emotion
    emotion_summary: Dict[str, int]  # emotion -> count

class AgentChatRequest(BaseModel):
    message: str
    session_ids: Optional[List[str]] = None
    session_emotions: Optional[Dict[str, Dict]] = None  # session_id -> emotion data

    class Config:
        json_schema_extra = {
            "example": {
                "message": "El paciente tiene ansiedad y le cuesta dormir por las noches. ¿Qué me recomienda?",
                "session_ids": ["session_123"],
                "session_emotions": {
                    "session_123": {
                        "timeline": {
                            "0": "happy",
                            "3": "happy",
                            "7": "neutral"
                        },
                        "emotion_summary": {
                            "happy": 2,
                            "neutral": 1
                        }
                    }
                }
            }
        }

@app.post("/api/agent/chat")
async def send_message(request: AgentChatRequest):
    """Enviar mensaje al agente y obtener respuesta"""
    try:
        # Obtener respuesta del agente
        session_id = request.session_ids[0] if request.session_ids else None
        agent_response = agent.process_message(
            message=request.message,
            session_id=session_id,
            session_emotions=request.session_emotions
        )
        return {"message": agent_response}
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- DEBUG: Imprimir rutas registradas ---
print("\n--- Rutas Registradas ---")
for route in app.routes:
    if hasattr(route, 'path'):
        print(f"Path: {route.path}, Name: {route.name}, Methods: {', '.join(route.methods) if hasattr(route, 'methods') else 'N/A'}")
print("-------------------------")
# --- FIN DEBUG ---

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
