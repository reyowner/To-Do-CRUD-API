from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel
from typing import List
import os

# FastAPI app setup
app = FastAPI()

# Setup templates & static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database setup (SQLite)
DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# To-Do model for database
class ToDoDB(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)

# Create the database
Base.metadata.create_all(bind=engine)

# Pydantic model for validation
class ToDoCreate(BaseModel):
    task: str

class ToDoResponse(ToDoCreate):
    id: int

# Serve the main page
@app.get("/")
def home(request: Request):
    session = SessionLocal()
    todos = session.query(ToDoDB).all()
    session.close()
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

# Create a to-do
@app.post("/todos", response_model=ToDoResponse)
def create_todo(todo: ToDoCreate):
    session = SessionLocal()
    new_todo = ToDoDB(task=todo.task)
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    session.close()
    return new_todo

# Get all to-dos
@app.get("/todos", response_model=List[ToDoResponse])
def get_todos():
    session = SessionLocal()
    todos = session.query(ToDoDB).all()
    session.close()
    return todos

# Retrieve a single to-do
@app.get("/todos/{todo_id}", response_model=ToDoResponse)
def get_todo(todo_id: int):
    session = SessionLocal()
    todo = session.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    session.close()
    if not todo:
        raise HTTPException(status_code=404, detail="To-Do not found")
    return todo

# Update a to-do
@app.put("/todos/{todo_id}", response_model=ToDoResponse)
def update_todo(todo_id: int, todo: ToDoCreate):
    session = SessionLocal()
    existing_todo = session.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    if not existing_todo:
        session.close()
        raise HTTPException(status_code=404, detail="To-Do not found")
    existing_todo.task = todo.task
    session.commit()
    session.refresh(existing_todo)
    session.close()
    return existing_todo

# Delete a to-do
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    session = SessionLocal()
    todo = session.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    if not todo:
        session.close()
        raise HTTPException(status_code=404, detail="To-Do not found")
    session.delete(todo)
    session.commit()
    session.close()
    return {"message": "To-Do deleted successfully"}
