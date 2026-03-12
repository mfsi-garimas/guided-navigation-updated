
# Guided-nav2.0

# Guided-nav2.0

## Project Overview
Guided-nav2.0 is an agentic, modular web automation and navigation platform. It leverages LLMs (Large Language Models) and a graph-based agent architecture to interpret user commands, automate web actions, and manage user roles and data. The project is designed for extensibility, maintainability, and integration with modern web technologies and cloud services.

---

## Features
- Browser extension for natural language web automation
- Backend with modular, agentic architecture (LangGraph compatible)
- Multi-agent orchestration (interpret, multi-step, select elements, supervisor)
- LLM integration (OpenAI, Gemini, etc.)
- Role-based access and user management
- Vector search and retrieval (Qdrant)
- Message queue support (RabbitMQ, Redis)
- Extensible, testable codebase

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repo-url>
cd Guided-nav2.0
```

### 2. Python Environment
```bash
python3 -m venv .venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
- Copy `.env.example` to `.env` and fill in your secrets (OpenAI, Gemini, Qdrant, RabbitMQ, Redis, etc.)

### 5. Start Backend Server
```bash
uvicorn app.main:app --reload --port 8001
```

### 6. Frontend Extension
- Go to your browser's extensions page
- Enable Developer Mode
- Load `app/extensions/` as an unpacked extension

---


## Folder Structure & Description

```
Guided-nav2.0/
├── app/
│   ├── agents/              # Agent classes (interprete, multi-step, select)
│   ├── config/              # Configuration loaders (env, logging, Qdrant, RabbitMQ, Redis)
│   ├── constants/           # Project-wide constants
│   ├── exceptions/          # Custom exception classes and handlers
│   ├── extensions/          # Browser extension files (content.js, manifest.json)
│   ├── graph/               # Graph orchestration (state, graph definition)
│   ├── llms/                # LLM client implementations (OpenAI, Gemini)
│   ├── models/              # Data models
│   ├── nodes/               # Node functions for graph steps (interprete, select_elements, multi_step)
│   ├── prompts/             # Prompt templates for agents
│   ├── repository/          # Data repositories (SQL, vector)
│   ├── routes/              # Modular FastAPI route files (health, interprete, select_elements, multi_step, main)
│   ├── schemas/             # Pydantic schemas for validation
│   ├── services/            # Service layer (core, IAM, message queue)
│   ├── tools/               # Utility tools (LLM client, config, agent tools)
│   └── workers/             # Background workers (ingestion)
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker build file
├── docker-compose.yml       # Docker orchestration
├── README.md                # Project documentation
├── LICENSE.md               # License information
└── CONTRIBUTING.md          # Contribution guidelines
```

---

## Key Components


### Agents (`app/agents/`)
- **interprete_agent.py**: Interprets user commands and webpage context
- **multi_step_agent.py**: Plans multi-step form interactions
- **select_elements_agent.py**: Selects relevant DOM elements for actions


### Config (`app/config/`)
- **env_config.py**: Loads environment variables from `.env`
- **log_config.py**: Logging setup



### Extensions (`app/extensions/`)
- **content.js**: Main browser extension logic (DOM extraction, API calls, UI)
- **manifest.json**: Extension manifest



### Graph (`app/graph/`)
- **interprete_graph.py**: Interprete agent workflow graph
- **select_elements_graph.py**: Select elements agent workflow graph
- **multistep_graph.py**: Multi-step agent workflow graph
- **state.py**: Graph state management


### Nodes (`app/nodes/`)
- **interprete_node.py**: Node function for interprete agent
- **select_elements_node.py**: Node function for select elements agent
- **multi_step_node.py**: Node function for multi-step agent


### LLMs (`app/llms/`)
- **openai_chat_client.py**: OpenAI API integration
- **gemini_chat_client.py**: Gemini API integration


### Prompts (`app/prompts/`)
- **interpret_prompt.py**: Prompt templates for interpretation
- **multi_step_prompt.py**: Prompt templates for multi-step agent
- **select_element_prompt.py**: Prompt templates for element selection


### Routes (`app/routes/`)
- **health_route.py**: Health check endpoint
- **interprete_route.py**: Interprete agent API endpoint
- **select_elements_route.py**: Select elements agent API endpoint
- **multi_step_route.py**: Multi-step agent API endpoint
- **main.py**: FastAPI app entry point (includes all routers)



### Tools (`app/tools/`)
- **llm_client.py**: LLM API wrapper
- **interprete_agent_tools.py**: Tools for the interprete agent
- **select_element_tools.py**: Tools for element selection
- **config.py**: Config utilities

---



## Usage

1. Start the backend server:
	```bash
	uvicorn app.main:app --reload
	```
2. Load the browser extension in your browser (see Installation step 6)
3. Interact with the chatbot UI to automate web actions
4. Use API endpoints for agentic workflows, retrieval, and user management

---

## Testing
- Run unit and integration tests (if available)
- Use FastAPI docs (`/docs`) for API exploration

---

## Contribution
- See `CONTRIBUTING.md` for guidelines
- PRs and issues welcome!

---

## License
- See `LICENSE.md` for details

---

