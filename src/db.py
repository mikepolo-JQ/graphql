import os

from dynaconf import settings
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

database_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
engine = create_engine("sqlite:///file.db")

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()
