from __future__ import annotations

import sqlite3
from typing import Iterator, List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from app.db import get_db, init_db

class ItemIn(BaseModel):
    name: str


class ItemOut(BaseModel):
    id: int
    name: str


app = FastAPI(title="Nano Banana")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/items", response_model=List[ItemOut])
def list_items(
        conn: sqlite3.Connection = Depends(get_db)
) -> List[ItemOut]:
    cur = conn.execute("SELECT id, name FROM items ORDER BY id")
    rows = cur.fetchall()
    return [
        {"id": r["id"],"name": r["name"]} for r in rows]


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(
        item_id: int,
        conn: sqlite3.Connection = Depends(get_db)
) -> ItemOut:
    cur = conn.execute("SELECT id, name FROM items WHERE id = ?", (item_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": row["id"], "name": row["name"]}


@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(item: ItemIn, conn: sqlite3.Connection = Depends(get_db)) -> ItemOut:
    cur = conn.execute("INSERT INTO items (name) VALUES (?)", (item.name,))
    item_id = cur.lastrowid
    conn.commit()
    return {"id": item_id, "name": item.name}


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, conn: sqlite3.Connection = Depends(get_db)) -> None:
    cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    conn.commit()
    return None

