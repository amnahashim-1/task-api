# Task API

A simple RESTful Task Management API built using **FastAPI**.

## Features

- Create a new task
- View all tasks
- View a single task
- Update an existing task
- Delete a task
- Health check endpoint
- Interactive Swagger documentation

## Technologies Used

- Python 3
- FastAPI
- Uvicorn
- Pydantic

## Installation

Clone the repository:

```bash
git clone https://github.com/amnahashim-1/task-api.git
```

Go to the project folder:

```bash
cd task-api
```

Install dependencies:

```bash
pip install fastapi uvicorn
```

Run the server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Home |
| GET | /health | Health Check |
| GET | /tasks | Get all tasks |
| GET | /tasks/{task_id} | Get one task |
| POST | /tasks | Create task |
| PUT | /tasks/{task_id} | Update task |
| DELETE | /tasks/{task_id} | Delete task |

---

## Example Response

```json
{
  "id": 1,
  "title": "Study Backend",
  "done": false
}
```
## Swagger UI

![Swagger UI](swagger.png)
## Author

# AI vs Me

## My Prompt

Build a Task API using FastAPI in Python with an in-memory list (no database). Implement GET /, GET /health, GET /tasks, GET /tasks/{id}, POST /tasks, PUT /tasks/{id}, and DELETE /tasks/{id}. Return the correct HTTP status codes (200, 201, 204, 400, 404), validate input, and include Swagger documentation at /docs.

## What the AI did better

- The AI added more comments and documentation.
- The AI used response models and type hints throughout the code.
- The AI organized the code into clear sections, making it easier to read.

## What the AI got wrong

- The AI used `completed` instead of the required `done` field.
- It added an extra `description` field that was not part of the assignment.
- It returned FastAPI's default validation format unless it was manually customized.

## What my prompt forgot

I forgot to specify the exact task model (`id`, `title`, `done`) and the exact JSON format for error responses, so the AI made its own design choices.

## Prompt Improvement

I improved my prompt by specifying the exact task fields, required HTTP status codes, validation rules, and JSON error format.
**Amna Hashim**
