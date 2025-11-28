import sys
import uuid

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import insert, select, text
from sqlalchemy.orm import Session

from database import get_db, items

app = FastAPI()

# User input model (no ID)
class ItemCreate(BaseModel):
    name: str
    price: float

# Full item model (ID included)
class Item(ItemCreate):
    id: str

@app.post("/items")
def create_item(item_data: ItemCreate, db: Session = Depends(get_db)):
    item_id = str(uuid.uuid4())
    item = Item(id=item_id, **item_data.model_dump())

    db.execute(text(f"INSERT INTO items VALUES ('{item.id}', '{item.name}', {item.price})"))
    db.commit()

    return {"message": "Item created", "item": item}

@app.get("/items/{item_id}")
def get_item(item_id: str, db: Session = Depends(get_db)):
    row = db.execute(text(f"select * from items where id = '{item_id}'"))
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    return row.fetchone()._asdict()

@app.get("/items")
def list_items(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * from items"))
    return [row._asdict() for row in result]

@app.get("/top")
def top(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * from items"))
    selected_items = [Item(**row._asdict()) for row in result]
    for item in selected_items:
        item_largest = True
        for item1 in selected_items:
            if item1.price > item.price:
                item_largest = False
        if item_largest:
            return item




    return selected_items