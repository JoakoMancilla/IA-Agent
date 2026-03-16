<div align="center">

<h1>IA-Agent</h1>

**Multi-agent AI assistant powered by Fireworks AI**

[![Python](https://img.shields.io/badge/Python-3.11+-6F2EE7?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-601EF8?style=flat-square)](https://langchain-ai.github.io/langgraph/)
[![Fireworks AI](https://img.shields.io/badge/Fireworks-AI-5313F8?style=flat-square)](https://fireworks.ai)
[![License](https://img.shields.io/badge/license-MIT-4A0BF8?style=flat-square)](LICENSE)

</div>

---

## ¿Qué es?

IA-Agent es un asistente de línea de comandos que orquesta múltiples agentes especializados para responder preguntas complejas. Un supervisor analiza cada mensaje del usuario, construye un plan de ejecución y delega a los agentes necesarios — sin loops, sin comportamiento impredecible.

```
You › en base a mis certificados, me conviene esta oferta? https://...

                              ▹ web_agent → rag_agent
                              ▹ web_agent  1/2
                         ⚙ TOOL: fetch_url ejecutado
                              ▹ rag_agent  2/2
                         ⚙ TOOL: consultar_documentos (Postgres)
                              ▹ sintetizando

╭─────────────────────────── IA-Agent ───────────────────────────╮
│  Considerando tus certificados en desarrollo de software...    │
╰────────────────────────────────────────────────────────────────╯
```

---

## Arquitectura

```
Usuario
  │
  ▼
Supervisor  ◄──────────────────────┐
  │                                │
  │  crea plan deterministico      │
  │  [web_agent, rag_agent, ...]   │
  │                                │
  ├──► web_agent   🌐 ─────────────┤
  ├──► rag_agent   📄 ─────────────┤
  └──► math_agent  🧮 ─────────────┘
          │
          ▼
      síntesis final → Usuario
```

El **supervisor** es el cerebro: usa el LLM una sola vez para crear el plan, luego lo ejecuta de forma determinística. Una vez que todos los agentes terminan, sintetiza los resultados en una respuesta única y coherente.

---

## Agentes

| Agente | Función | Herramienta |
|--------|---------|-------------|
| `web_agent` | Navega URLs proporcionadas por el usuario | `fetch_url` |
| `rag_agent` | Consulta documentos personales (CV, certificados, PDFs) | `consultar_documentos` (Postgres + pgvector) |
| `math_agent` | Cálculos, promedios, estadísticas | `promedio_de_notas` |

---

## Stack

- **[LangGraph](https://langchain-ai.github.io/langgraph/)** — orquestación del grafo de agentes
- **[Fireworks AI](https://fireworks.ai)** — modelos LLM (`llama-v3p3-70b` para supervisor, `qwen3-8b` para agentes)
- **[LangChain](https://langchain.com)** — abstracción de agentes y tools
- **[Rich](https://rich.readthedocs.io)** — UI de terminal
- **PostgreSQL + pgvector** — base vectorial para RAG

---

## Instalación

```bash
git clone https://github.com/tu-usuario/ia-agent
cd ia-agent
pip install -r requirements.txt
```

Configura tus variables de entorno en `.env`:

```env
FIREWORKS_API_KEY=your_key_here
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

Ejecuta:

```bash
python main.py
```

---

## Estructura

```
ia-agent/
├── main.py                  # Entry point y UI de terminal
├── graph/
│   └── graph_manage.py      # Definición del grafo LangGraph
├── agent/
│   ├── supervisor.py        # Orquestador principal
│   ├── rag_agent.py         # Agente de documentos
│   ├── math_agent.py        # Agente matemático
│   └── web_agent.py         # Agente web
└── tools/
    ├── rag_tool.py          # consultar_documentos
    ├── math_tools.py        # promedio_de_notas
    └── web_tools.py         # fetch_url
```

---

## Decisiones de diseño

**El supervisor no usa LLM para seguir el plan** — solo para crearlo. Esto elimina loops y comportamiento no determinístico. Una vez que existe el plan `["web_agent", "rag_agent"]`, se ejecuta en orden sin consultar al modelo.

**Los agentes siempre reciben el mensaje original del usuario** — no el último mensaje del estado, que podría ser la respuesta de otro agente. Esto evita context bleed entre agentes.

**Los bloques `<think>` de Qwen3 se limpian antes de la síntesis** — el modelo de razonamiento genera thinking interno que LangChain captura en `content`. Se filtra con regex antes de pasar los resultados al supervisor.

---

<div align="center">

Made with 🟣 by **JoakoMancillaDev**

</div>
