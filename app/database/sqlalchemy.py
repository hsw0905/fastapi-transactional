from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, scoped_session

from app.config import config

engine = create_engine(
    url=config.DB_URL,
    echo=config.DB_ECHO,
    pool_pre_ping=config.DB_PRE_PING,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

session = scoped_session(session_factory=session_factory)
