import requests
import json
import asyncio
from app.services.therapeutic_agent import TherapeuticAgent

async def test_agent():
    # Cargar datos de prueba
    with open('test_data.json', 'r') as f:
        test_data = json.load(f)
    
    # Crear instancia del agente
    agent = TherapeuticAgent()
    
    # Generar recomendaciones
    recommendations = await agent.generate_recommendations(
        patient_id=test_data['patient_id'],
        therapist_id=test_data['therapist_id'],
        emotion_data=test_data['emotion_data']
    )
    
    # Imprimir resultados
    print("\n=== Resultados del Análisis ===")
    print(f"\nPaciente: {recommendations['patient_id']}")
    print(f"Terapeuta: {recommendations['therapist_id']}")
    print(f"\nEmoción Dominante: {recommendations['dominant_emotion']}")
    print("\nAnálisis:")
    print(recommendations['analysis']['analysis'])
    print("\nRecomendaciones:")
    print(recommendations['recommendations'])
    print("\nRecursos:")
    for resource in recommendations['resources']:
        print(f"\n- {resource['title']}")
        print(f"  {resource['snippet']}")

def test_api():
    # Cargar datos de prueba
    with open('test_data.json', 'r') as f:
        test_data = json.load(f)
    
    # URL del endpoint
    url = f"http://localhost:8000/api/therapeutic-agent/analyze/{test_data['therapist_id']}/{test_data['patient_id']}"
    
    # Realizar petición
    response = requests.post(
        url,
        json={'emotion_data': test_data['emotion_data']},
        headers={'Content-Type': 'application/json'}
    )
    
    # Verificar respuesta
    if response.status_code == 200:
        print("\n=== Prueba de API Exitosa ===")
        print("\nRespuesta del servidor:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"\nError en la petición: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print("=== Probando Agente Directamente ===")
    asyncio.run(test_agent())
    
    print("\n=== Probando API ===")
    test_api() 