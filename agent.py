import os
import google.generativeai as genai
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from typing import List, Dict, Optional
import json
from datetime import datetime

# Load environment variables
load_dotenv()

class TherapeuticAgent:
    def __init__(self):
        # Initialize Gemini
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash') #1.5 flash importante
        
        # Agent personality and context
        self.personality = {
            "role": "Especialista en psicoterapia y análisis emocional",
            "approach": "Empático y profesional",
            "style": "Sugerente y no impositivo",
            "context": "Experto en análisis de patrones emocionales y recomendaciones personalizadas"
        }
        
        # Initialize search engine
        self.search_engine = DDGS()

    def _get_web_recommendations(self, query: str) -> List[Dict]:
        """Search for relevant therapeutic tools and recommendations"""
        try:
            results = self.search_engine.text(query, max_results=3)
            return [{"title": r["title"], "snippet": r["body"]} for r in results]
        except Exception as e:
            print(f"Error in web search: {e}")
            return []

    def _format_prompt(self, patient_data: Dict, web_results: List[Dict]) -> str:
        """Format the prompt for the Gemini model"""
        web_context = "\n".join([f"- {r['title']}: {r['snippet']}" for r in web_results])
        
        return f"""Como especialista en psicoterapia y análisis emocional, analiza los siguientes datos del paciente y proporciona recomendaciones personalizadas.

Datos del paciente:
{json.dumps(patient_data, indent=2, ensure_ascii=False)}

Información adicional de recursos terapéuticos:
{web_context}

Por favor, proporciona recomendaciones considerando:
1. Patrones emocionales observados
2. Herramientas y técnicas que podrían ser útiles
3. Sugerencias para el manejo emocional
4. Recursos adicionales que podrían ser beneficiosos

Recuerda que estas son recomendaciones basadas en el análisis y no verdades absolutas."""

    def get_recommendations(self, patient_data: Dict) -> Dict:
        """Generate personalized recommendations based on patient data"""
        # Search for relevant therapeutic tools
        search_query = f"herramientas terapéuticas para {patient_data.get('current_emotion', 'manejo emocional')}"
        web_results = self._get_web_recommendations(search_query)
        
        # Generate recommendations using Gemini
        prompt = self._format_prompt(patient_data, web_results)
        response = self.model.generate_content(prompt)
        
        return {
            "recommendations": response.text,
            "sources": web_results,
            "timestamp": patient_data.get("timestamp")
        }

    def _format_chat_prompt(self, message: str, session_id: Optional[str] = None, session_emotions: Optional[Dict[str, Dict]] = None) -> str:
        """Format the prompt for chat interactions"""
        # Formatear el contexto de la sesión
        context_parts = []
        if session_id:
            context_parts.append(f"Sesión ID: {session_id}")
        else:
            context_parts.append("Nueva sesión")

        # Formatear los datos de emociones de la sesión si están disponibles
        if session_emotions:
            context_parts.append("\nAnálisis Emocional de la Sesión:")
            for session_id, emotion_data in session_emotions.items():
                context_parts.append(f"\nSesión {session_id}:")
                
                # Resumen de emociones
                if 'emotion_summary' in emotion_data:
                    summary = emotion_data['emotion_summary']
                    context_parts.append("Resumen de emociones:")
                    for emotion, count in summary.items():
                        context_parts.append(f"- {emotion}: {count} veces")
                
                # Timeline de emociones
                if 'timeline' in emotion_data:
                    timeline = emotion_data['timeline']
                    context_parts.append("\nEvolución temporal de emociones:")
                    for timestamp, emotion in timeline.items():
                        context_parts.append(f"- {timestamp}: {emotion}")
        
        context = "\n".join(context_parts)
        
        return f"""Como especialista en psicoterapia y análisis emocional, responde al siguiente mensaje.

Contexto:
{context}

Mensaje:
{message}

IMPORTANTE: Todas tus respuestas deben ser RECOMENDACIONES y SUGERENCIAS, nunca afirmaciones absolutas o diagnósticos definitivos. 
Debes enfatizar que estas son sugerencias basadas en el análisis de los datos disponibles.

Por favor, proporciona una respuesta:
1. Empática y profesional
2. Basada en principios terapéuticos
3. Sugerente y no impositiva
4. Considerando el contexto proporcionado, especialmente el análisis emocional de la sesión
5. Enfocada en recomendaciones y sugerencias, no en diagnósticos definitivos

Recuerda que eres un asistente terapéutico y debes mantener un tono profesional y de apoyo."""

    def process_message(self, message: str, session_id: Optional[str] = None, session_emotions: Optional[Dict[str, Dict]] = None) -> str:
        """Process a chat message and generate a response"""
        print(f"[Agent] Processing message for session_id: {session_id}, message: {message}")
        if session_emotions:
            print(f"[Agent] Session emotions provided: {json.dumps(session_emotions, indent=2)}")
        
        try:
            # Format the prompt for chat
            prompt = self._format_chat_prompt(message, session_id, session_emotions)
            print(f"[Agent] Formatted prompt: {prompt}")
            
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            print(f"Error processing message: {e}")
            return "Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta nuevamente." 