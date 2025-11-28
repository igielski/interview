from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean
from sqlalchemy import insert, select
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# ---------------------------
# Database setup (NO ORM)
# ---------------------------
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

metadata = MetaData()

items = Table(
    "items",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String),
    Column("price", Float),
)

metadata.create_all(engine)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()