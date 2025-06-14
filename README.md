# EmotionAI Therapeutic Agent

Este agente proporciona recomendaciones personalizadas basadas en el análisis de datos emocionales de un paciente, usando la API de Gemini (modelo Flash) y búsqueda web para enriquecer las sugerencias.

## Cambios recientes
- Ahora utiliza el modelo `gemini-1.5-flash-latest` para mayor velocidad y menos problemas de cuota.
- El endpoint espera un JSON con la clave `emotion_data` en la raíz.
- El análisis y las recomendaciones se generan en inglés, usando los mismos nombres de emociones que la base de datos.
- Se agregó un script de prueba (`test_agent.py`) que permite probar el agente tanto directamente como vía API.
- Se agregó un `.gitignore` para evitar subir archivos sensibles y temporales.



## Estructura del endpoint
- **POST** `/api/therapeutic-agent/analyze/{therapist_id}/{patient_id}`
- **Body:**
   ```json
   {
     "emotion_data": {
       "timeline": { "0": "happy", ... },
       "emotion_summary": { "happy": 3, ... }
     }
   }
   ```

## Notas
- El agente funciona con emociones en inglés (como en la base de datos de EmotionAI).
- El modelo Gemini Flash es más rápido y tiene menos restricciones de cuota que Pro.

## Características

- Análisis de patrones emocionales
- Recomendaciones personalizadas
- Integración con Gemini AI
- Búsqueda de recursos terapéuticos mediante DuckDuckGo
- API REST para integración con la aplicación móvil


## Integración con la App Móvil

El agente está diseñado para ser consumido por la aplicación móvil EmotionAI. La integración se realiza mediante llamadas HTTP al endpoint de recomendaciones.

## Notas Importantes

- Las recomendaciones son sugerencias basadas en el análisis y no deben ser consideradas como verdades absolutas
- El agente está diseñado para complementar, no reemplazar, la atención profesional
- Se recomienda validar las recomendaciones con un profesional de la salud mental 