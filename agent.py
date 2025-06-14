import os
import google.generativeai as genai
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from typing import List, Dict, Optional
import json

# Load environment variables
load_dotenv()

class TherapeuticAgent:
    def __init__(self):
        # Initialize Gemini
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
        
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