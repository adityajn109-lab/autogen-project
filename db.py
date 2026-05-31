from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres.ocfgvgjdjvtbcpwilaws:Adityajn109#@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"


engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
