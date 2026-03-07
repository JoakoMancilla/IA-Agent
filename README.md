# 🤖 IA-Agent

![Python](https://img.shields.io/badge/python-3.10+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-blue)
![LangChain](https://img.shields.io/badge/LangChain-AI%20Framework-green)
![CLI](https://img.shields.io/badge/CLI-Rich-purple)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

**IA-Agent** es un agente de inteligencia artificial con capacidades **RAG (Retrieval-Augmented Generation)** diseñado para consultar y responder preguntas utilizando **documentos propios**.

El proyecto combina:

- **LLMs**
- **RAG**
- **PostgreSQL + pgvector**
- **LangChain**
- **CLI estilizado con Rich**

Esto permite construir asistentes de IA capaces de **consultar conocimiento personalizado almacenado localmente**.

---

# 🚀 Características

### 🧠 Agente de IA
- Conversación con un LLM
- Arquitectura preparada para agregar herramientas (tools)
- Modular y extensible

### 📚 Sistema RAG
- Consulta documentos propios
- Recuperación semántica de contexto
- Generación de respuestas basada en conocimiento

### 🗄 Base de datos vectorial
- PostgreSQL
- extensión **pgvector**
- almacenamiento persistente de embeddings

### 📄 Procesamiento de documentos
- carga de documentos locales
- división automática en chunks
- generación de embeddings

### 💻 CLI estilizado
- interfaz de terminal construida con **Rich**
- salida visual clara
- interacción simple desde consola

---

# 🏗 Arquitectura

```
Usuario (CLI)
      │
      ▼
   AI Agent
      │
      ├── LLM
      │
      ├── Tools
      │
      └── RAG Pipeline
            │
            ├── Document Loader
            ├── Text Splitter
            ├── Embeddings
            └── PostgreSQL + pgvector
```

### Flujo del sistema

1️⃣ Se cargan documentos locales  
2️⃣ Se dividen en fragmentos (chunks)  
3️⃣ Cada fragmento se transforma en **embedding**  
4️⃣ Se almacenan en **PostgreSQL + pgvector**  
5️⃣ El usuario hace una pregunta  
6️⃣ Se recupera el contexto más relevante  
7️⃣ El LLM genera la respuesta

---

# 📦 Stack tecnológico

- **Python**
- **LangChain**
- **PostgreSQL**
- **pgvector**
- **Rich**
- **Google Gemini / OpenAI API**

---

# ⚙️ Instalación

## 1️⃣ Clonar repositorio

```bash
git clone https://github.com/JoakoMancilla/IA-Agent.git
cd IA-Agent
```

---

## 2️⃣ Crear entorno virtual

Linux / Mac

```bash
python -m venv venv
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

## 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Variables de entorno

Crear archivo `.env`

```
GOOGLE_API_KEY=tu_api_key
DATABASE_URL=postgresql://usuario:password@localhost:5432/tu_base
```

---

# 🗄 Configuración PostgreSQL + pgvector

Dentro de PostgreSQL ejecutar:

```sql
CREATE EXTENSION vector;
```

Luego crear la base de datos que usará el proyecto.

---

# 📚 Ingesta de documentos

Para indexar documentos en la base vectorial:

```bash
python ingest.py
```

Este proceso:

- carga documentos
- los divide en fragmentos
- genera embeddings
- los guarda en PostgreSQL

---

# 💬 Ejecutar el agente

```bash
python main.py
```

Ejemplo de consulta:

```
> ¿Qué experiencia tiene Joaquín en inteligencia artificial?
```

El agente:

1. busca los fragmentos relevantes
2. entrega el contexto al modelo
3. genera una respuesta basada en los datos

---

# 🖥 Demo CLI

Ejemplo de interacción:

```
╭────────────────────────────────────╮
│          IA-Agent CLI              │
╰────────────────────────────────────╯

> ¿Qué experiencia tengo en desarrollo de videojuegos?

🔎 Buscando contexto en la base vectorial...

📄 Contexto encontrado:
- Experiencia en Unity
- Desarrollo de juegos 2D y 3D
- Uso de motores como Godot y Unreal

🤖 Respuesta:
Tienes experiencia desarrollando videojuegos con motores como Unity y Godot...
```
<img width="641" height="339" alt="IA-Agent" src="https://github.com/user-attachments/assets/09d53d84-d05a-4e0e-884c-0f0a959c7108" />

---

# 📁 Estructura del proyecto

```
IA-Agent
│
├── main.py
│
├── rag/
│   ├── ingest.py
│   ├── retriever.py
│
├── agent/
│   ├── agent.py
│   └── tools.py
│
├── db/
│   └── vector_store.py
│
├── utils/
│
├── requirements.txt
└── README.md
```

---

# 🎯 Objetivo del proyecto

Este proyecto fue desarrollado como parte del aprendizaje de:

- **AI Agents**
- **RAG systems**
- **bases de datos vectoriales**
- **LangChain**
- **interfaces CLI para herramientas de IA**

El código está diseñado para ser **simple, modular y fácil de extender**.

---

# 🔮 Mejoras futuras

- arquitectura **multi-agente**
- integración con **LangGraph**
- interfaz **web**
- **streaming de respuestas**
- más loaders de documentos
- memoria conversacional persistente
- tools especializadas por dominio

---

# 📜 Licencia

MIT License

---

💡 Proyecto creado como parte de la exploración en **AI Agents, RAG systems y asistentes de conocimiento personalizados**.
