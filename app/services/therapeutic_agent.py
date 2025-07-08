import os
import google.generativeai as genai
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from typing import List, Dict, Optional
from datetime import datetime
from langdetect import detect

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

    async def generate_recommendations(self, patient_id: str, therapist_id: str, emotion_data: Dict, user_message: str) -> Dict:
        """Generates a clinically-focused, context-rich response for the specific patient, considering the user's message and language."""
        # Analyze patient data
        analysis = await self.analyze_patient_data(patient_id, therapist_id, emotion_data)
        dominant_emotion = max(emotion_data['emotion_summary'].items(), key=lambda x: x[1])[0]
        resources = await self.search_therapeutic_resources(
            dominant_emotion,
            f"patient {patient_id} with {dominant_emotion}"
        )

        # Detect language of the user message
        try:
            user_lang = detect(user_message)
        except Exception:
            user_lang = "en"

        emotional_timeline = self._format_emotion_timeline(emotion_data['timeline'])
        emotion_summary = self._format_emotion_summary(emotion_data['emotion_summary'])
        resources_formatted = self._format_resources(resources)

        prompt = f"""
You are a clinical psychotherapy assistant. Your role is to provide the most clinically relevant, context-rich, and precise answers to the clinician's questions about a specific patient.

**Instructions:**
- Your top priority is to answer the clinician's question directly and precisely, using all available context.
- You may elaborate and provide additional clinical context, interpretation, or relevant insights if they help the clinician, but do not lose focus on the original question.
- Do NOT provide step-by-step plans, generic advice, or lists of actions.
- Focus on clinical reasoning, interpretation, and evidence-based insights, always tailored to the patient's context.
- Never state absolute truths or diagnoses; always use suggestive, professional, and non-imposing language.
- If you are unsure, say so.
- Your answer MUST be in the same language as the clinician's question (detected language: {user_lang}). If the question is in Spanish, answer in Spanish. If in English, answer in English. If in another language, answer in that language. Do NOT translate the question. Do NOT explain your language choice. Just answer directly in the detected language.

**Patient Context:**
- Patient ID: {patient_id}
- Therapist ID: {therapist_id}
- Dominant Emotion: {dominant_emotion}
- Emotional Timeline:
{emotional_timeline}
- Emotion Summary:
{emotion_summary}

**Clinical Analysis:**
{analysis['analysis']}

**Relevant Therapeutic Resources:**
{resources_formatted}

**Clinician's Question (original language):**
{user_message}

**IMPORTANT:**
Your answer should be concise, clinically focused, and context-aware. Do NOT provide a list of steps or a plan. Do NOT give absolute statements or diagnoses. Always maintain a professional, supportive, and suggestive tone. Prioritize answering the question, but you may elaborate if it adds clinical value.
"""

        print(f"\n--- Prompt para Generación de Respuesta Clínica del Paciente {patient_id} ---\n{prompt}\n---")
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