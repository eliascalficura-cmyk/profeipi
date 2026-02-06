import os
import base64
import httpx
from fastapi import FastAPI, Query, Body
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

load_dotenv()

# CONFIGURACIÓN CRÍTICA v23.0
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY", "").strip().replace('"', '').replace("'", "")
ELEVEN_VOICE_ID = os.getenv("ELEVEN_VOICE_ID", "kgTZJF3nCUbUlPl0aChy").strip().replace('"', '').replace("'", "")

client = genai.Client(api_key=GEMINI_KEY)

app = FastAPI(title="PROFE IPI - ATM Future Solution Chile [v23.0]")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MEMORIA CONVERSACIONAL (In-Memory)
chat_sessions = {}

# CACHÉ DE RESPUESTAS (Optimización de velocidad)
response_cache = {}
MAX_CACHE_SIZE = 50

def get_cache_key(prompt: str) -> str:
    """Crear clave de caché normalizada"""
    # Remover modo y limpiar
    cleaned = prompt.lower().strip()
    cleaned = cleaned.replace('[mode: classroom]', '').replace('[mode: strategy]', '').strip()
    # Tomar primeros 100 caracteres para clave
    return cleaned[:100]

# PROMPT MAESTRO: IPINCE 6.0 [ULTRA_CONCISE_CHILEAN]
ATTENTION_FILTER_PROMPT = (
    "### IDENTIDAD: ERES EL PROFESOR PABLO IPINCE (PROFE IPI)\n"
    "Académico de élite. Tu regla de oro es la BREVEDAD EXTREMA.\n\n"
    
    "### PROTOCOLO DE CONCISIÓN:\n"
    "1. LÍMITE DE RESPUESTA: Prohibido responder más de 1 o 2 párrafos cortos (máximo 40-50 palabras en total).\n"
    "2. FOCO ÚNICO: Entrega solo UN concepto o dato clave a la vez. No satures al alumno.\n"
    "3. ESTILO: Directo, académico y de alto impacto. Si es necesario profundizar, hazlo en la siguiente interacción.\n\n"
    
    "#### MODO LOGIMASTER (AULA):\n"
    "Enseña con micro-píldoras de información. Una analogía corta + una pregunta de validación. Fin del turno.\n\n"
    
    "#### MODO ESTRATEGA (NEGOCIOS):\n"
    "Dato crudo, análisis de 1 línea y recomendación ejecutiva inmediata.\n\n"
    
    "### PROTOCOLO TÉCNICO:\n"
    "Usa el modo LOGIMASTER si detectas '[MODE: CLASSROOM]'. Sé impecable, conciso y elegante.\n\n"
    "### CONTEXTO_ACTUAL: "
)

class ChatRequest(BaseModel):
    prompt: str
    image_b64: Optional[str] = None
    session_id: str = "default_session"

async def generate_voice_elevenlabs(text):
    if not ELEVEN_API_KEY:
        return None
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
        headers = {"xi-api-key": ELEVEN_API_KEY, "Content-Type": "application/json"}
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.45, "similarity_boost": 0.80}
        }
        async with httpx.AsyncClient() as session:
            res = await session.post(url, json=payload, headers=headers, timeout=30.0)
            if res.status_code == 200:
                return base64.b64encode(res.content).decode("utf-8")
            return None
    except:
        return None

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>ERROR: index.html no encontrado</h1>"

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        prompt = request.prompt
        session_id = request.session_id
        
        # Verificar caché primero
        cache_key = get_cache_key(prompt)
        if cache_key in response_cache and len(cache_key) > 10:  # Solo cachear preguntas sustanciales
            print(f"\n💾 CACHE_HIT: {cache_key[:50]}...")
            cached_data = response_cache[cache_key]
            # Regenerar audio si es necesario (el audio no se cachea, solo el texto)
            audio_b64 = await generate_voice_elevenlabs(cached_data["response"])
            return {"response": cached_data["response"], "audio": audio_b64}
        
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
            
        print(f"\n📥 NEXUS_INCOMING [{session_id}]: {prompt}")
        
        contents = []
        # Historial
        for msg in chat_sessions[session_id][-6:]: # Mantenemos 6 turnos para balancear memoria/tokens
            contents.append({"role": msg["role"], "parts": [{"text": msg["text"]}]})
            
        # Entrada actual
        current_parts = [{"text": ATTENTION_FILTER_PROMPT + prompt}]
        
        if request.image_b64:
            img_data = request.image_b64.split(",")[-1]
            current_parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": img_data
                }
            })
            print("📸 Visual data detected in Optic Bridge")

        contents.append({"role": "user", "parts": current_parts})

        response = client.models.generate_content(
            model="gemini-2.0-flash", # Soporta Visión perfectamente
            contents=contents
        )
        texto_ia = response.text
        
        # Guardar en memoria  
        chat_sessions[session_id].append({"role": "user", "text": prompt})
        chat_sessions[session_id].append({"role": "model", "text": texto_ia})
        
        # Guardar en caché (solo si no está lleno)
        if len(response_cache) < MAX_CACHE_SIZE and len(cache_key) > 10:
            response_cache[cache_key] = {"response": texto_ia}
            print(f"💾 CACHE_STORED: {cache_key[:50]}... (Total: {len(response_cache)})")
        
        print(f"💬 NEXUS_RESPONSE: {texto_ia}")
        
        audio_b64 = await generate_voice_elevenlabs(texto_ia)
        return {"response": texto_ia, "audio": audio_b64}
        
    except Exception as e:
        print(f"❌ NEXUS_ERROR: {str(e)}")
        return {"response": f"Interferencia: {str(e)}", "audio": None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
