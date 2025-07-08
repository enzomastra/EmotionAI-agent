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

# --- DEBUG: Imprimir rutas registradas ---
print("\n--- Rutas Registradas ---")
for route in app.routes:
    if hasattr(route, 'path'):
        print(f"Path: {route.path}, Name: {route.name}, Methods: {', '.join(route.methods) if hasattr(route, 'methods') else 'N/A'}")
print("-------------------------")
# --- FIN DEBUG ---

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
