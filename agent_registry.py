from db import SessionLocal
from models import Agent
from autogen_agentchat.agents import AssistantAgent


# ✅ Create agent dynamically from DB
def create_agent_from_db(agent_name: str, tools, model_client):
    db = SessionLocal()

    try:
        agent_data = db.query(Agent).filter_by(name=agent_name).first()

        if not agent_data:
            raise ValueError(f"Agent '{agent_name}' not found")

        return AssistantAgent(
            name=agent_data.name,
            model_client=model_client,
            tools=tools,
            system_message=agent_data.system_message
        )

    finally:
        db.close()


# ✅ Agent Registry (Main Manager)
class AgentRegistry:

    def __init__(self, tools, model_client):
        """
        tools: ALL_TOOLS list
        model_client: Azure OpenAI client
        """
        self.tools = tools
        self.model_client = model_client

    def get(self, agent_name: str):
        """
        Returns a fresh agent instance from DB
        """
        return create_agent_from_db(
            agent_name,
            self.tools,
            self.model_client
        )

    def list_agents(self):
        """
        Returns all agent names from DB
        """
        db = SessionLocal()

        try:
            agents = db.query(Agent).all()
            return [a.name for a in agents]

        finally:
            db.close()