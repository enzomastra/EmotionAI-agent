import os
import google.generativeai as genai
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from typing import List, Dict, Optional
from datetime import datetime

class TherapeuticAgent:
    def __init__(self):
        # Cargar variables de entorno
        load_dotenv()
        
        # Configurar Gemini
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        
        # Configurar buscador
        self.search_engine = DDGS()
        
        # Personalidad del agente
        self.personality = {
            "role": "Psychotherapy and Emotional Analysis Specialist",
            "approach": "Empathetic and professional",
            "style": "Suggestive and non-imposing",
            "context": "Expert in emotional pattern analysis and personalized recommendations"
        }

    async def analyze_patient_data(self, patient_id: str, therapist_id: str, emotion_data: Dict) -> Dict:
        """Analyzes the specific patient's data"""
        prompt = f"""As a psychotherapy specialist, analyze the following data for patient {patient_id}:

Emotional Timeline:
{self._format_emotion_timeline(emotion_data['timeline'])}

Emotion Summary:
{self._format_emotion_summary(emotion_data['emotion_summary'])}

Please provide a detailed analysis considering:
1. Specific emotional patterns for this patient
2. Dominant emotions and their frequency
3. Possible triggers identified
4. Specific areas for improvement
5. Progress or changes over time

Provide a detailed but concise analysis, focused on this specific patient."""

        print(f"\n--- Prompt para Análisis del Paciente {patient_id} ---\n{prompt}\n---")
        response = self.model.generate_content(prompt)
        return {"analysis": response.text}

    async def search_therapeutic_resources(self, emotion: str, patient_context: str) -> List[Dict]:
        """Searches for relevant therapeutic resources for the specific patient"""
        query = f"therapeutic techniques for managing {emotion} in {patient_context}"
        try:
            results = self.search_engine.text(query, max_results=3)
            return [{"title": r["title"], "snippet": r["body"]} for r in results]
        except Exception as e:
            print(f"Error in web search: {e}")
            return []

    async def generate_recommendations(self, patient_id: str, therapist_id: str, emotion_data: Dict) -> Dict:
        """Generates personalized recommendations for the specific patient"""
        # Analyze patient data
        analysis = await self.analyze_patient_data(patient_id, therapist_id, emotion_data)
        
        # Get dominant emotion
        dominant_emotion = max(emotion_data['emotion_summary'].items(), key=lambda x: x[1])[0]
        
        # Search for patient-specific resources
        resources = await self.search_therapeutic_resources(
            dominant_emotion,
            f"patient {patient_id} with {dominant_emotion}"
        )
        
        # Generate personalized recommendations
        prompt = f"""As a psychotherapy specialist, provide personalized recommendations for patient {patient_id} based on:

Pattern Analysis:
{analysis['analysis']}

Therapeutic Resources:
{self._format_resources(resources)}

Dominant Emotion: {dominant_emotion}

Provide specific and relevant recommendations for this patient, such as:
1. Immediate strategies for managing {dominant_emotion}
2. Long-term personalized plan
3. Specific tools
4. Relevant additional resources

Remember these are suggestions, not absolute truths."""

        print(f"\n--- Prompt para Generación de Recomendaciones del Paciente {patient_id} ---\n{prompt}\n---")
        response = self.model.generate_content(prompt)
        
        return {
            "patient_id": patient_id,
            "therapist_id": therapist_id,
            "recommendations": response.text,
            "analysis": analysis,
            "resources": resources,
            "dominant_emotion": dominant_emotion,
            "timestamp": datetime.now()
        }

    def _format_emotion_timeline(self, timeline: Dict) -> str:
        """Formats the emotional timeline for the prompt"""
        return "\n".join([
            f"- Second {second}: {emotion}"
            for second, emotion in sorted(timeline.items())
        ])

    def _format_emotion_summary(self, summary: Dict) -> str:
        """Formats the emotion summary for the prompt"""
        return "\n".join([
            f"- {emotion}: {count} occurrences"
            for emotion, count in summary.items()
        ])

    def _format_resources(self, resources: List[Dict]) -> str:
        """Formats the resources for the prompt"""
        return "\n".join([
            f"- {r['title']}: {r['snippet']}"
            for r in resources
        ]) 