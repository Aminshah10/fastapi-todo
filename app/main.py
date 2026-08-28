from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi import Depends
from app.tasks.routes import router as task_routes
from app.users.routes import router as user_routes
from app.auth.routes import router as auth_routes

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
    version="0.0.2",
)
app.include_router(task_routes)
app.include_router(user_routes)
app.include_router(auth_routes)