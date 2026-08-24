from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.tasks.routes import router as task_routes

@asynccontextmanager
async def lifespan(app : FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")
    
app = FastAPI(
    lifespan=lifespan,
    title="Task Management API",
    description="""
    A RESTful API for creating, managing, updating, and tracking tasks.

    Features:
    - Create tasks
    - Retrieve tasks
    - Update tasks
    - Delete tasks
    - Track task completion status
    """,
    version="0.0.1",
)
app.include_router(task_routes)