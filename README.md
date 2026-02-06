# 🎓 PROFE IPI - Sistema de Asistente Educativo IA

Sistema inteligente de asistencia educativa con reconocimiento de voz y respuestas optimizadas para el área de logística y negocios.

## ✨ Características

- 🎤 **Reconocimiento de voz** en español chileno con activación por palabra clave
- 🤖 **IA potente** - Respuestas generadas con Gemini 2.0 Flash
- 🔊 **Voz natural** - Síntesis de voz con ElevenLabs
- ⚡ **Modo rápido** - Solo texto, 3x más rápido
- 💾 **Sistema de caché** - Respuestas instantáneas para preguntas frecuentes
- 🎨 **Interfaz premium** - Diseño glassmorphism con visualización 3D

## 🚀 Características de Rendimiento

### Optimizaciones Implementadas
- **Velocidad**: 3-5 segundos (modo normal), 2-3 segundos (modo rápido)
- **Precisión**: 85-95% en reconocimiento de voz
- **Caché**: Respuestas instantáneas (<1s) para preguntas repetidas
- **Timeouts optimizados**: 800ms silencio, 10s conexión, 7s activación

### Modos de Operación
1. **Modo Estrategia**: Análisis ejecutivo y recomendaciones de negocio
2. **Modo Aula (LogiMaster)**: Enseñanza pedagógica con micro-píldoras de información
3. **Modo Rápido**: Solo texto, sin audio para máxima velocidad

## 🎮 Cómo Usar

1. **Activar micrófono**: Click en "Iniciar_Cortex"
2. **Llamar al profesor**: Di "Profe" o "Profesor"
3. **Hacer pregunta**: El sistema muestra preview en tiempo real
4. **Recibir respuesta**: Con audio y texto (o solo texto en modo rápido)

### Palabras de Activación
- "Profe"
- "Profesor"
- "Oye Profe"
- "Hola Profe"
- "Profesor Ipince"

## 🔧 Variables de Entorno

```env
GEMINI_API_KEY=tu_api_key_de_gemini
ELEVEN_API_KEY=tu_api_key_de_elevenlabs
ELEVEN_VOICE_ID=kgTZJF3nCUbUlPl0aChy
```

### Obtener API Keys
- **Gemini**: https://makersuite.google.com/app/apikey
- **ElevenLabs**: https://elevenlabs.io/app/settings/api-keys

## 🛠️ Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/TU-USUARIO/profe-ipi.git
cd profe-ipi

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys

# Ejecutar
python main.py
```

Visita: http://localhost:8000

## 🌐 Despliegue en Vercel

Ver [implementation_plan.md](implementation_plan.md) para instrucciones detalladas de despliegue.

## 📊 Tecnologías Utilizadas

- **Backend**: FastAPI + Python 3.10+
- **IA**: Google Gemini 2.0 Flash
- **Voz**: ElevenLabs TTS
- **Frontend**: HTML5 + JavaScript + TailwindCSS
- **3D**: Three.js
- **Despliegue**: Vercel

## 📝 Estructura del Proyecto

```
profe-ipi/
├── main.py                 # Backend FastAPI
├── index.html              # Frontend + UI
├── requirements.txt        # Dependencias Python
├── vercel.json            # Configuración Vercel
├── .env                   # Variables de entorno (no subir a git)
├── .gitignore             # Archivos a ignorar
└── README.md              # Este archivo
```

## 🎯 Roadmap

- [x] Sistema de activación por palabra clave
- [x] Optimización de timeouts y velocidad
- [x] Modo rápido sin audio
- [x] Sistema de caché
- [ ] Modo offline con cache persistente
- [ ] Configuración de palabras clave personalizables
- [ ] Dashboard de métricas de uso
- [ ] Soporte multi-idioma

## 👨‍💻 Autor

**ATM Chile** - Proyecto Profe IPI 2026

Desarrollado con ❤️ para la educación en logística y negocios.

## 📄 Licencia

Proyecto privado - Todos los derechos reservados

---

**Versión**: 3.0 - Optimizado para Velocidad y Precisión  
**Última actualización**: Febrero 2026
