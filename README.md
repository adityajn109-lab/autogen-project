✅ PHASE 0: SYSTEM DESIGN & SETUP
Explain:
- Overall system architecture (frontend + backend + agents + RAG)
- Role of Azure AI Foundry
- Why we use AutoGen instead of raw APIs
- Difference between LLM, Agent, Tool, RAG
- High-level data flow (user → agent → tools → response)

Tasks:
- Setup Python 3.12 + FastAPI
- Setup Azure OpenAI model (Foundry)
- Create project folder structure

Deliverables:
- Working FastAPI server
- Azure-connected model config


✅ PHASE 1: CORE AGENT SYSTEM
Explain:
- What is an Agent in AutoGen
- AssistantAgent vs UserProxyAgent
- LLM configuration (Azure-specific)
- System prompt design

Tasks:
- Create basic AssistantAgent
- Connect to Azure model
- Build /chat API
- Execute simple queries

Deliverables:
- Agent responding via API


✅ PHASE 2: TOOL SYSTEM (AGENT CAPABILITIES)
Explain:
- What are tools in agentic systems
- FunctionTool concept
- How LLM decides tool calling

Tasks:
- Create basic tools (calculator, string tool)
- Build dynamic Python tool loader (exec)
- Attach tools to agent
- Test tool calling

Deliverables:
- Agent calling tools dynamically


✅ PHASE 3: RAG MEMORY SYSTEM (COST-OPTIMIZED)
Explain:
- What is RAG
- Why not fine-tuning
- Chunking, embeddings, retrieval

Tasks:
- Build DocumentMemory class
- Implement chunking logic
- Use SentenceTransformer (local embeddings)
- Store in ChromaDB
- Query top-k chunks
- Build context injection

Deliverables:
- Agent answering from uploaded documents


✅ PHASE 4: FILE PROCESSING + MEMORY INTEGRATION
Explain:
- File ingestion pipelines
- How document memory works in real systems
- Why context is injected into user message (not system)

Tasks:
- Build PDF/TXT loader
- Process uploaded files
- Add caching via file hash
- Integrate with RAG pipeline

Deliverables:
- Upload + query file functionality


✅ PHASE 5: MULTI-AGENT SYSTEM (CORE OF AGENTIC AI)
Explain:
- Why multiple agents
- Planner vs Executor roles
- Team orchestration

Tasks:
- Create PlannerAgent
- Create ExecutorAgent
- Build Team class (sequential execution)
- Pass messages between agents

Deliverables:
- Multi-agent workflow execution


✅ PHASE 6: TEAM ORCHESTRATION (ENTERPRISE CONCEPT)
Explain:
- Team types (RoundRobin, Selector, Orchestrator)
- Termination conditions
- Agent roles in teams

Tasks:
- Implement simple RoundRobin team
- Add max step limit
- Add stop condition
- Build TeamFactory (basic version)

Deliverables:
- Reusable team execution engine


✅ PHASE 7: STREAMING ARCHITECTURE (/run-stream clone)
Explain:
- Why streaming is needed
- NDJSON vs WebSockets
- Event-driven AI responses

Tasks:
- Create streaming endpoint
- Emit events (start, agent_step, tool_call, result)
- Integrate team.run() with streaming
- Handle async responses

Deliverables:
- Real-time streaming API


✅ PHASE 8: FRONTEND INTEGRATION (REACT UI)
Explain:
- How frontend consumes streaming APIs
- Chat UI vs workflow UI

Tasks:
- Build chat interface
- Build workflow interface
- Parse NDJSON events
- Show agent steps in UI

Deliverables:
- End-to-end working system (UI + backend)


✅ PHASE 9: ADVANCED TOOLS (REAL-WORLD POWER)
Explain:
- External tool integration
- Browser automation use cases

Tasks:
- Build Playwright tool
- Add API-based tool
- Add runtime configs

Deliverables:
- Agent performing real-world tasks


✅ PHASE 10: MEMORY EXTENSIONS
Explain:
- Difference between short-term and long-term memory
- Semantic memory systems

Tasks:
- Add conversation memory
- Store interaction history
- Retrieve past context

Deliverables:
- Memory-aware agents


✅ PHASE 11: PRODUCTION-STYLE FEATURES
Explain:
- Scaling agent systems
- Reliability patterns

Tasks:
- Add logging
- Add retry logic
- Add caching
- Model selection handling

Deliverables:
- Stable system


✅ PHASE 12: EXPERT/ENTERPRISE FEATURES
Explain:
- MCP (Model Context Protocol)
- Guardrails systems
- Prompt versioning
- HITL (Human-in-the-loop)

Tasks:
- Implement one advanced feature (optional)
- Design scalable architecture

Deliverables:
- Enterprise-level understanding


🧠 HOW TO USE THIS WITH YOUR AI AGENT
Now your workflow should be:

✅ Step-by-step usage
Prompt 1:
Explain PHASE 0 in detail including architecture and setup.

Prompt 2:
Explain PHASE 1 with code examples and implementation.

Prompt 3:
Now help me implement Day 1 tasks step-by-step.


👉 Repeat for every phase

🔥 FINAL RESULT
If you follow this:
✅ You’ll rebuild your company system from scratch
✅ You’ll deeply understand each layer
✅ You’ll be able to modify / extend real systems confidently

🚀 If You Want Next Step
I can also generate:
✅ A super prompt per phase (very detailed)
✅ Exact code implementations per phase
✅ Complete Azure Foundry integration template
✅ Full TeamFactory + AgentFactory clone


agent gallery summary -
Backend
Framework: FastAPI + Uvicorn, Python 3.12

Startup: On app start, connects to PostgreSQL via a connection pool (PostgresDB), optionally initializes Phoenix/OpenTelemetry tracing, then registers all routers. JWT Bearer token middleware validates every request. CORS is open to allow frontend connections.

Agent System: Built on Microsoft AutoGen (autogen_agentchat, autogen_core, autogen_ext). Supported agent types are AssistantAgent, CodeExecutorAgent, MultimodalWebSurfer, FileSurfer, VideoSurfer, and MagenticOneGroupChat. Agents are created by AgentFactory which loads the agent config from DB, attaches MCP tools, builds a system message, loads RAG memory and user memory, and returns a fully configured AutoGen agent object.

Team System: Teams are groups of agents that run together. Supported team types are RoundRobinGroupChat (agents take turns), SelectorGroupChat (LLM picks next speaker based on a selector prompt), and MagenticOneGroupChat (orchestrator-driven complex task solving). Teams have participants (agents with roles) and termination conditions (max messages or stop keyword). TeamFactory builds the AutoGen team object from DB config. Teams are cached per user session and reset between runs.

Main Streaming Endpoint: POST /teams/{team_id}/run-stream accepts a user task, user ID, optional files, model selection, and runtime config. It processes files, builds or reuses a cached team, queries RAG and user memory, prepends context to the user message, then streams NDJSON events back to the frontend. Events include progress stages (team_building_start, file_processing, file_ready, agent_creating, agent_ready, stream_started) followed by actual agent messages (TextMessage, ToolCallRequestEvent, ToolCallExecutionEvent, TaskResult).

Individual Agent Chat: POST /agent/{workflow_id}/{user_id}/{agent_id}/chat handles single-agent conversations with file upload support, guardrail validation on input and output, interaction recording, and memory storage.

Memory System: Three layers. First, DocumentMemory is a local in-memory vector store built from uploaded files — files are chunked, embedded using SentenceTransformer (BGE, GTE, E5, Nomic, or MxBai models), and queried per request to inject relevant chunks as context. Second, user memory is long-term conversation history stored in an external memory microservice and retrieved via semantic search. Third, RAG memory is knowledge base content retrieved from the same external service via a /api/query/ endpoint. All memory is injected into the user message as a context block (not as system messages, to support Anthropic compatibility).

MCP (Model Context Protocol): Agents can be connected to external tool servers via HTTP or STDIO transports. MCP configs are stored in the DB. At agent creation time, the MCP server is connected, tools are discovered, and each tool is wrapped as an AutoGen FunctionTool with a dynamically generated typed Python signature. The MCPWorkbenchManager handles session lifecycle.

Custom Tools: Users can write Python functions directly in the UI. These are stored in the DB with a name, description, JSON schema for parameters, and the raw Python code. At runtime, the code is compiled via ast.parse + exec and wrapped as a FunctionTool. Tools support a runtime_config_schema for fields like PAT tokens that should be prompted at runtime and never stored.

Guardrails: Agents can have guardrails assigned (stored in lookup_values table). Before and after agent execution, the message is sent to the external memory service's /guardrails/validate endpoint. If validation fails, an HTTP 400 is raised with the violation reasons.

Prompt Versioning: Every agent has a prompt table entry and a prompt_version table with semantic versioning (1.0.0, patch/minor/major). When a prompt is updated, a new version is created and marked active. Old versions are preserved and can be reactivated.

Human-in-the-Loop (HITL): An optional workflow mode where after each agent step, the frontend receives the agent output and recommended options, the user approves or modifies, and execution continues. Managed by HITLWorkflowManager.

Agent Cancellation: A CancellationToken is passed into team.run_stream(). A separate router allows the frontend to cancel a running workflow by team/user ID.

Export: Agents and teams can be exported as Postman collections or Azure AI Foundry deployment configs.

Routers registered: user, agent, team, interaction, lookup, category, mcp, tools, guardrails, config, logs, ado (Azure DevOps), export, foundry deployments, chat, browser_stream, workflow, models_service, import, utils, agent_cancellation.

Database Tables (PostgreSQL):

agent_master — agent config (name, type, description, additional_params JSON, context, category, created_by, modified_by)

prompt + prompt_version — system prompts with semantic versioning

team + team_participant + termination_condition — team structure

mcp_config + mcp_tools — MCP server configs and tool definitions

agent_tools — agent to tool mapping

tools — custom Python tools with code and parameter schema

interaction — chat history with feedback/voting

user_master — users with admin flag

category — agent categories

lookup_types + lookup_values — dropdown data (agent types, team types, guardrail options, etc.)

guardrail — agent to guardrail mapping

runtime_config_store — per-user per-session runtime tool configs

Auth: Azure AD JWT validation middleware. Every request (except OPTIONS) must carry a Bearer token. The token is also forwarded to the external memory microservice for all memory/RAG/guardrail calls.

Frontend
Framework: React 18, React Router v6, Framer Motion for page transitions, Azure MSAL for Azure AD SSO (optional — falls back gracefully if not configured).

Routes:

/ and /login → Login page (Azure AD or simple auth)

/discover → Discovery page, shows all enabled agents as cards with creator, category, description

/home → Home page, select an agent and chat with it individually

/workflow → Workflow page, select a team and run multi-agent workflows with streaming

/about → About page

/tools → Tools Library for managing custom Python tools

Key UI Flows:

Individual agent chat: User selects an agent from AgentList, opens ChatInterface, types a message, optionally uploads files, selects a model from ModelSettingsSidebar, and sends. The frontend POSTs to the chat endpoint and displays the streamed response. Thumbs up/down voting is available on each response.

Team workflow: User opens WorkFlowInterface, selects a team, optionally uploads files and configures runtime tool values via RuntimeConfigForm, then submits a task. The frontend connects to the NDJSON stream endpoint and parses events. Progress events update a progress bar and status messages. Agent messages are rendered in WFChatInterface with ExecutionSteps showing tool calls and results. HITL mode shows HITLBubble for human approval steps.

Agent management: CreateAgent form supports all agent types with type-specific parameters (headless/start_page for WebSurfer, base_path for FileSurfer, video paths for VideoSurfer, code executor settings for CodeExecutorAgent). UpdateAgent allows editing prompt with change type (patch/minor/major) and change summary for versioning. Prompt version history is viewable and any version can be reactivated.

Team management: CreateTeam and EditTeam allow configuring team type, selector prompt, participants with roles and speak order, and termination conditions. DeleteTeam removes the team.

MCP management: MCPConfig allows adding HTTP or STDIO MCP servers, probing them to discover available tools, selecting which tools to enable, and attaching the config to an agent. MCPConfigList shows all configs. MCPToolManager shows tools per config.

Tools Library: ToolsLibrary shows all public tools plus the user's private tools. CreateToolForm allows writing Python code directly with a name, description, and parameter schema. Tools can be assigned to agents.

Guardrails: ConfigureGuardrails allows assigning guardrail types to an agent from the lookup values.

Admin: AdminPanel allows admins to add/manage users.

Services layer: Every backend resource has a corresponding service file (agentService, teamService, mcpService, toolService, guardrailsService, categoryService, lookupService, modelService, authService, etc.) that wraps fetch/axios calls with auth headers. An apiInterceptor handles token expiration globally and redirects to login.

Model selection: ModelSettingsSidebar lets users pick a model provider (Azure OpenAI, OpenAI, Anthropic) and specific model, temperature, and max output tokens. This is passed per-request to the backend which creates a parameterized model client for that request.

Key Data Flows
File upload in team workflow: Files arrive at the stream endpoint → SHA256 hashed → compared to cache → if new, load_chunks_from_uploads_memory() parses the file (PDF via PyMuPDF/pdfplumber, DOCX via python-docx, Excel via openpyxl, CSV, XML, JMX, JTL, WSDL, images) → chunks are batch-embedded using local SentenceTransformer → stored in DocumentMemory → cached by file hash → on each request, DocumentMemory.query(user_task) retrieves top-k relevant chunks → build_memory_context_for_user_message() formats them → prepended to the user task before sending to the team.

Team run: POST /teams/{team_id}/run-stream → check runtime config for unconfigured tools → process files → check team cache → if cache miss, ConfigDynamic() → TeamFactory.create() → for each participant agent, AgentFactory.create_With_Memory(skip_external_memory=True) → build AutoGen team object → cache it → reset team state → query file memory + RAG + user memory → build context message → team.run_stream(context_message) → serialize each AutoGen message → yield as NDJSON → frontend renders.

MCP tool call: Agent receives user message → LLM decides to call a tool → AutoGen calls the FunctionTool → tool_func() calls MCPManager.get_executor() → executor.call_tool(tool_name, payload) → HTTP POST to MCP server → result returned → format_tool_result() normalizes it → returned to LLM as tool result.

Memory storage: After agent responds → add_memory_with_chunking() → sanitize content → split into 1000-char overlapping chunks → for each chunk, POST /add-memory to external memory service with JWT → stored in mem0-style vector DB → available for future RAG queries.

Tech Stack
Backend: Python 3.12, FastAPI, Uvicorn, Microsoft AutoGen (autogen_agentchat 0.7.2, autogen_core, autogen_ext), psycopg2, asyncpg, SQLAlchemy 2.0, Pydantic v2, sentence-transformers, numpy, httpx, PyMuPDF, pdfplumber, python-docx, openpyxl, Playwright, OpenTelemetry, loguru

Frontend: React 18, React Router v6, Framer Motion, Azure MSAL (@azure/msal-react), Axios

Database: PostgreSQL (primary), SQLite (legacy)

LLM Providers: Azure OpenAI, Anthropic Claude, OpenAI (switchable per request)

Embeddings: Local SentenceTransformer (BAAI/bge-small-en-v1.5 default, configurable)

Infrastructure: Docker (both services), Nginx (frontend reverse proxy), Azure App Service compatible, Azurite for local blob storage emulation

run using - uvicorn app:app --reload