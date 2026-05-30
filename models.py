from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from db import Base

# ✅ USERS
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)


# ✅ CHAT HISTORY
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    message = Column(Text)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


# ✅ TOOLS
class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(Text)
    system_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    