from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from agent import TherapeuticAgent
import uvicorn

app = FastAPI(title="EmotionAI Therapeutic Agent")
agent = TherapeuticAgent()

class PatientData(BaseModel):
    current_emotion: str
    emotion_history: list
    timestamp: str
    additional_context: Optional[Dict] = None

@app.post("/recommendations")
async def get_recommendations(patient_data: PatientData):
    try:
        recommendations = agent.get_recommendations(patient_data.dict())
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 