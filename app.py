import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio
from tools.loader import load_tools_from_string,load_tools_from_db
from tools.static_tools import calculator, num_play;
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from models import Tool, Conversation
from db import SessionLocal
from agent_registry import AgentRegistry

load_dotenv()


app = FastAPI(title="jarvis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from agent_registry import AgentRegistry

model_client = AzureOpenAIChatCompletionClient(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION"),
    azure_deployment=os.getenv("AZURE_DEPLOYMENT"),
    model="gpt-4.1-mini"
)


class ChatRequest(BaseModel):
    message: str
    agent: str = "jarvis"   # default# Define the expected structure of the incoming JSON request for pydantic model, pydantic model is a technique of sending the data in a specefic format and validating it before processing it.

class ToolRequest(BaseModel):
    code: str

class AgentRequest(BaseModel):
    name: str
    description: str
    system_message: str

ALL_TOOLS = [calculator, num_play] + load_tools_from_db()
# print("LOADED TOOLS FROM DB:", [t.__name__ for t in ALL_TOOLS])
registry = AgentRegistry(ALL_TOOLS,model_client)



def get_agent():
    return AssistantAgent(
            name="Jarvis",
            model_client=model_client,
            tools=ALL_TOOLS,
            system_message="""
            You are Jarvis.

            Rules:
            - Always respond in Hinglish.
            - If the question involves numbers, math, or calculations:
            → ALWAYS call the correct tool
            → NEVER calculate manually
            - Choose the MOST relevant tool based on the task
            """
        )




# @app.post("/chat")
# async def chat(request: ChatRequest):
#     if not request.message.strip():
#         raise HTTPException(status_code=400, detail="Message cannot be empty")
    
#     try:
        
#         # 2. Initiate the chat
#         # Note: AutoGen's initiate_chat is synchronous, but running it 
#         # inside an 'async def' handler in FastAPI prevents it from stalling the event loop.
#         assistant = get_agent()
#         result = await assistant.run(task=request.message)

#         # 3. Extract the last message from the chat history
#         all_messages = result.messages

#         if all_messages:
#             final_reply = all_messages[-1].content
#         else:
#             final_reply = "No response generated."

#         # 4. Return standard Python dictionary (FastAPI auto-converts to JSON)
#         return {
#             "status": "success",
#             "reply": final_reply
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e)) chat request before db was added


# @app.post("/chat")
# async def chat(request: ChatRequest):

#     db = SessionLocal()

#     try:
#         # agent = get_agent() before registry is created we were creating a new agent instance for every request, but now we will create the agent once and reuse it for every request using registry
#         agent = registry.get(request.agent) #when registry is maded, we can get the agent instance by its name using registry.get() method. This way we can reuse the same agent instance for multiple requests, which is more efficient than creating a new instance for every request.
#         result = await agent.run(task=request.message)

#         reply = result.messages[-1].content

#         # ✅ Save conversation
#         convo = Conversation(
#             user_id=1,  # temporary
#             message=request.message,
#             response=reply
#         )

#         db.add(convo)
#         db.commit()

#         return {
#             "status": "success",
#             "reply": reply
#         }

#     finally:
#         db.close()

@app.post("/chat")
async def chat(request: ChatRequest):

    db = SessionLocal()

    try:
        # ✅ agent DB se aaega
        agent = registry.get(request.agent) #here we are fetching the agent instance from the registry using the agent name provided in the request. This allows us to reuse the same agent instance for multiple requests, which is more efficient than creating a new instance for every request. 

        result = await agent.run(task=request.message)
        reply = result.messages[-1].content

        # ✅ save chat
        convo = Conversation(
            user_id=1,
            message=request.message,
            response=reply
        )
        db.add(convo)
        db.commit()

        return {
            "status": "success",
            "reply": reply
        }

    finally:
        db.close()
    
    


@app.post("/add-tool")
async def add_tool(request: ToolRequest):
    global ALL_TOOLS

    db = SessionLocal()

    try:
        new_tools = load_tools_from_string(request.code)

        existing_names = {t.__name__ for t in ALL_TOOLS}

        for tool in new_tools:
            # ✅ Save to DB
            db_tool = Tool(
                name=tool.__name__,
                code=request.code
            )
            db.add(db_tool)

            # ✅ Add to runtime
            if tool.__name__ not in existing_names:
                ALL_TOOLS.append(tool)

        db.commit()

        return {
            "status": "success",
            "tools": [t.__name__ for t in new_tools]
        }

    finally:
        db.close()


@app.get("/agents")
def list_agents():
    return {
        "agents": registry.list_agents()
    }

from models import Agent
from db import SessionLocal

@app.post("/add-agent")
async def add_agent(request: AgentRequest):
    db = SessionLocal()

    try:
        new_agent = Agent(
            name=request.name,
            description=request.description,
            system_message=request.system_message
        )

        db.add(new_agent)
        db.commit()

        return {
            "status": "success",
            "agent": request.name
        }

    finally:
        db.close()