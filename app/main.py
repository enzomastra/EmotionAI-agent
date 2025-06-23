from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import therapeutic_agent

app = FastAPI(
    title="EmotionAI Therapeutic Agent",
    description="Agente terapéutico para análisis emocional y recomendaciones personalizadas",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(
    therapeutic_agent.router,
    prefix="/api/agent",
    tags=["therapeutic-agent"]
)

@app.get("/")
async def root():
    return {
        "message": "Bienvenido al Agente Terapéutico de EmotionAI",
        "version": "1.0.0",
        "status": "active"
    } 