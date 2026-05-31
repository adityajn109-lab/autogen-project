# import os
# import asyncio
# from dotenv import load_dotenv

# from autogen_agentchat.agents import AssistantAgent
# from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

# load_dotenv()

# # ✅ Azure client
# model_client = AzureOpenAIChatCompletionClient(
#     azure_endpoint=os.getenv("AZURE_ENDPOINT"),
#     api_key=os.getenv("AZURE_API_KEY"),
#     api_version=os.getenv("AZURE_API_VERSION"),
#     azure_deployment=os.getenv("AZURE_DEPLOYMENT"),
#     model="gpt-4.1-mini"
# )

# def calculator(a: int, b: int) -> int:
#     """Add two numbers"""
#     return a - b

# # ✅ Agent (pass function directly)
# agent = AssistantAgent(
#     name="jarvis",
#     model_client=model_client,
#     tools=[calculator],  # ✅ THIS IS CORRECT
#     system_message="""
#     You are an AI assistant.

#     RULES:
#     - Always use the calculator tool for math
#     - Never calculate manually
#     """
# )

# # ✅ Run
# async def main():
#     result = await agent.run(task="Add 20 and 30")
#     print(result.messages[-1].content)

# asyncio.run(main())

# from db import engine

# try:
#     conn = engine.connect()
#     print("✅ DB Connected Successfully")
#     conn.close()
# except Exception as e:
#     print("❌ Error:", e)

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("./bge-small-en-v1.5")
print(model.encode("Hello world"))