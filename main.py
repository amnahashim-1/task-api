from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


# In-memory task list
tasks = [
    {
        "id": 1,
        "title": "Study Backend",
        "done": False
    },
    {
        "id": 2,
        "title": "Buy Milk",
        "done": False
    },
    {
        "id": 3,
        "title": "Exercise",
        "done": True
    }
]


# Model for creating a task
class Task(BaseModel):
    title: str


# Model for updating a task
class UpdateTask(BaseModel):
    title: str
    done: bool


# Home endpoint
@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# Health endpoint
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks


# Get a single task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# Create a new task
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):

    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


# Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: UpdateTask):

    for task in tasks:

        if task["id"] == task_id:

            task["title"] = updated_task.title
            task["done"] = updated_task.done

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# Delete a task
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):

    for task in tasks:

        if task["id"] == task_id:

            tasks.remove(task)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )