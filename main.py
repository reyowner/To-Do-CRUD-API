from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, ToDoDB
from schemas import ToDoCreate, ToDoResponse
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Setup templates & static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

def get_db():
    """
    Dependency function to provide a database session.
    Ensures proper cleanup after each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_model=None)
def home(request: Request, db: Session = Depends(get_db)):
    """
    Serve the homepage with a list of all to-dos.

    Parameters:
    - request (Request): The FastAPI request object.
    - db (Session): The database session.

    Returns:
    - HTML template response displaying the list of to-dos.
    """
    try:
        todos = db.query(ToDoDB).all()
        return templates.TemplateResponse("index.html", {"request": request, "todos": todos})
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch To-Dos")

@app.post("/todos", response_model=ToDoResponse, status_code=201)
def create_todo(todo: ToDoCreate, db: Session = Depends(get_db)):
    """
    Create a new to-do item.

    Parameters:
    - todo (ToDoCreate): Pydantic model containing task data.
    - db (Session): Database session.

    Returns:
    - ToDoResponse: The created to-do item with an assigned ID.

    Raises:
    - HTTP 500 if the to-do creation fails.
    """
    new_todo = ToDoDB(task=todo.task)
    db.add(new_todo)
    try:
        db.commit()
        db.refresh(new_todo)
        return new_todo
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create To-Do")

@app.get("/todos", response_model=List[ToDoResponse])
def get_todos(db: Session = Depends(get_db)):
    """
    Retrieve all to-dos from the database.

    Parameters:
    - db (Session): The database session.

    Returns:
    - List[ToDoResponse]: A list of all stored to-dos.

    Raises:
    - HTTP 500 if retrieval fails.
    """
    try:
        return db.query(ToDoDB).all()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch To-Dos")

@app.get("/todos/{todo_id}", response_model=ToDoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single to-do item by its ID.

    Parameters:
    - todo_id (int): ID of the to-do item.
    - db (Session): The database session.

    Returns:
    - ToDoResponse: The requested to-do item if found.

    Raises:
    - HTTP 404 if the to-do is not found.
    """
    todo = db.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-Do not found")
    return todo

@app.put("/todos/{todo_id}", response_model=ToDoResponse)
def update_todo(todo_id: int, todo: ToDoCreate, db: Session = Depends(get_db)):
    """
    Update an existing to-do item.

    Parameters:
    - todo_id (int): ID of the to-do item to update.
    - todo (ToDoCreate): Pydantic model with updated task data.
    - db (Session): The database session.

    Returns:
    - ToDoResponse: The updated to-do item.

    Raises:
    - HTTP 404 if the to-do is not found.
    - HTTP 500 if the update fails.
    """
    existing_todo = db.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    if not existing_todo:
        raise HTTPException(status_code=404, detail="To-Do not found")
    
    existing_todo.task = todo.task
    try:
        db.commit()
        db.refresh(existing_todo)
        return existing_todo
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update To-Do")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Delete a to-do item.

    Parameters:
    - todo_id (int): ID of the to-do item to delete.
    - db (Session): The database session.

    Returns:
    - dict: Success message.

    Raises:
    - HTTP 404 if the to-do is not found.
    - HTTP 500 if the deletion fails.
    """
    todo = db.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-Do not found")
    
    try:
        db.delete(todo)
        db.commit()
        return {"message": "To-Do deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete To-Do")
