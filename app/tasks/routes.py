from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.tasks.models import TaskModel
from app.users.models import UserModel
from app.tasks.schemas import *
from app.auth.jwt_auth import get_authenticated_user

router = APIRouter(tags=["tasks"])

DB_DEPENDENCY = Depends(get_db)
AUTHENTICATED_USER_DEPENDENCY = Depends(get_authenticated_user)


@router.get("/tasks", response_model=list[ResponseTaskSchema])
def retrieve_all_tasks(
    db: Session = DB_DEPENDENCY,
    user: UserModel = AUTHENTICATED_USER_DEPENDENCY,
    completed: bool | None = Query(
        default=None, description="filter tasks by their completion status"
    ),
    limit: int = Query(
        default=10, gt=0, le=100, description="limit the number of tasks returned"
    ),
    offset: int = Query(default=0, ge=0, description="offset for pagination"),
):
    if completed is not None:
        result = (
            db.query(TaskModel)
            .filter_by(user_id=user.id, is_done=completed)
            .offset(offset)
            .limit(limit)
            .all()
        )
    else:
        result = (
            db.query(TaskModel)
            .filter_by(user_id=user.id)
            .offset(offset)
            .limit(limit)
            .all()
        )
    return result


@router.get("/tasks/{task_id}", response_model=ResponseTaskSchema)
def retrieve_task_detail(
    task_id: int = Path(..., gt=0),
    db: Session = DB_DEPENDENCY,
    user: UserModel = AUTHENTICATED_USER_DEPENDENCY,
):
    result = (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id, TaskModel.user_id == user.id)
        .one_or_none()
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return result


@router.post(
    "/tasks", response_model=ResponseTaskSchema, status_code=status.HTTP_201_CREATED
)
def create_task(
    task: CreateTaskSchema,
    db: Session = DB_DEPENDENCY,
    user: UserModel = AUTHENTICATED_USER_DEPENDENCY,
):
    new_task = TaskModel(**task.model_dump())
    new_task.user_id = user.id
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.patch("/tasks/{task_id}", response_model=ResponseTaskSchema)
def update_task(
    task: UpdateTaskSchema,
    task_id: int = Path(..., gt=0),
    db: Session = DB_DEPENDENCY,
    user: UserModel = AUTHENTICATED_USER_DEPENDENCY,
):
    result = (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id, TaskModel.user_id == user.id)
        .one_or_none()
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(result, key, value)

    db.commit()
    db.refresh(result)
    return result


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int = Path(..., gt=0),
    db: Session = DB_DEPENDENCY,
    user: UserModel = AUTHENTICATED_USER_DEPENDENCY,
):
    result = (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id, TaskModel.user_id == user.id)
        .one_or_none()
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    db.delete(result)
    db.commit()
    return None  # noqa: PLR1711, RET501