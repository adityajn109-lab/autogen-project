import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent

load_dotenv()

app = FastAPI(title="Adii's jarvis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_config = {
    "config_list": [
        {
            "model": os.getenv("AZURE_DEPLOYMENT"),  # or your Azure deployment name
            "api_key": os.getenv("AZURE_API_KEY"),
            "base_url": os.getenv("AZURE_ENDPOINT"),
            "api_type": "azure",
            "api_version": os.getenv("AZURE_API_VERSION"),
        }
    ],
    "temperature": 0.7,
}

class ChatRequest(BaseModel): # Define the expected structure of the incoming JSON request for pydantic model, pydantic model is a technique of sending the data in a specefic format and validating it before processing it.
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        assistant = AssistantAgent(
            name="Jarvis",
            llm_config=llm_config,
            system_message="You are a helpful and concise AI assistant. who talks in hinglish only"
        )

        user_proxy = UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",  # Must be NEVER for API setups
            max_consecutive_auto_reply=1,
            code_execution_config=False
        )
        # 2. Initiate the chat
        # Note: AutoGen's initiate_chat is synchronous, but running it 
        # inside an 'async def' handler in FastAPI prevents it from stalling the event loop.
        chat_result = user_proxy.initiate_chat(
            recipient=assistant,
            message=request.message,
            clear_history=True 
        )

        # 3. Extract the last message from the chat history
        all_messages = chat_result.chat_history
        
        if all_messages:
            final_reply = all_messages[-1]["content"]
        else:
            final_reply = "No response generated."

        # 4. Return standard Python dictionary (FastAPI auto-converts to JSON)
        return {
            "status": "success",
            "reply": final_reply
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))