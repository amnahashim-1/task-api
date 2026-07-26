"""
Task API — FastAPI application with an in-memory data store (no database).

Endpoints:
    GET    /             -> API welcome/info
    GET    /health        -> health check
    GET    /tasks          -> list all tasks
    GET    /tasks/{id}     -> get a single task
    POST   /tasks          -> create a task
    PUT    /tasks/{id}     -> update a task
    DELETE /tasks/{id}     -> delete a task

Run with:
    pip install fastapi uvicorn
    uvicorn main:app --reload

Swagger docs available at:  http://127.0.0.1:8000/docs
ReDoc docs available at:    http://127.0.0.1:8000/redoc
"""

from itertools import count
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator


# --------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------

class TaskBase(BaseModel):
    title: str = Field(..., description="Title of the task (required, non-empty)")
    description: Optional[str] = Field(None, description="Optional longer description")
    completed: bool = Field(False, description="Whether the task is completed")

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value: str) -> str:
        if value is None or not value.strip():
            raise ValueError("title must not be empty")
        return value.strip()


class TaskCreate(TaskBase):
    """Payload for creating a task."""
    pass


class TaskUpdate(TaskBase):
    """Payload for updating a task (full replace of the editable fields)."""
    pass


class Task(TaskBase):
    id: int = Field(..., description="Unique identifier of the task")


# --------------------------------------------------------------------------
# App setup
# --------------------------------------------------------------------------

app = FastAPI(
    title="Task API",
    description="A simple in-memory Task management API built with FastAPI.",
    version="1.0.0",
)

# In-memory store
tasks_db: List[Task] = []
_id_counter = count(1)  # auto-incrementing IDs starting at 1


def _find_task_index(task_id: int) -> int:
    """Return the index of a task in tasks_db, or -1 if not found."""
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            return index
    return -1


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------

@app.get("/", tags=["Meta"], status_code=status.HTTP_200_OK)
def read_root():
    """Welcome/info endpoint."""
    return {
        "message": "Welcome to the Task API",
        "docs": "/docs",
        "health": "/health",
        "tasks": "/tasks",
    }


@app.get("/health", tags=["Meta"], status_code=status.HTTP_200_OK)
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.get("/tasks", response_model=List[Task], tags=["Tasks"], status_code=status.HTTP_200_OK)
def get_tasks():
    """Return the list of all tasks."""
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"], status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    """Return a single task by its ID."""
    index = _find_task_index(task_id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    return tasks_db[index]


@app.post("/tasks", response_model=Task, tags=["Tasks"], status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    """Create a new task."""
    new_task = Task(id=next(_id_counter), **task_in.model_dump())
    tasks_db.append(new_task)
    return new_task


@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"], status_code=status.HTTP_200_OK)
def update_task(task_id: int, task_in: TaskUpdate):
    """Update an existing task."""
    index = _find_task_index(task_id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")

    updated_task = Task(id=task_id, **task_in.model_dump())
    tasks_db[index] = updated_task
    return updated_task


@app.delete("/tasks/{task_id}", tags=["Tasks"], status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """Delete a task by its ID."""
    index = _find_task_index(task_id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    tasks_db.pop(index)
    return None


# --------------------------------------------------------------------------
# Validation error -> 400 instead of FastAPI's default 422
# --------------------------------------------------------------------------

from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    By default FastAPI returns 422 for request validation errors (e.g. empty
    title, missing required field). The task spec calls for 400 instead.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)