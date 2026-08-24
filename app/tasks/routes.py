from fastapi import APIRouter, Depends, Path, Query, HTTPException, status
from app.tasks.models import TaskModel
from app.tasks.schemas import *
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["tasks"])

DB_DEPENDENCY = Depends(get_db)

@router.get("/tasks", response_model=list[ResponseTaskSchema])
def retrieve_all_tasks(db:Session = DB_DEPENDENCY, 
                       completed :bool | None = Query(default=None, description="filter tasks by their completion status"),
                       limit :int = Query(default=10, gt=0, le=100, description="limit the number of tasks returned"),
                       offset :int = Query(default=0, ge=0, description="offset for pagination")):
    if completed is not None:
        result = db.query(TaskModel).filter(TaskModel.is_done == completed).offset(offset).limit(limit).all()
    else:
        result = db.query(TaskModel).offset(offset).limit(limit).all()
    return result

@router.get("/tasks/{task_id}", response_model=ResponseTaskSchema)
def retrieve_task_detail(task_id : int = Path(..., gt=0), db:Session = DB_DEPENDENCY):
    result = db.query(TaskModel).filter(TaskModel.id == task_id).one_or_none()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    return result

@router.post("/tasks", response_model=ResponseTaskSchema, status_code=status.HTTP_201_CREATED)
def create_task(task:CreateTaskSchema, db:Session = DB_DEPENDENCY):
    new_task = TaskModel(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.patch("/tasks/{task_id}", response_model=ResponseTaskSchema)
def update_task(task:UpdateTaskSchema, task_id:int = Path(..., gt=0), db:Session = DB_DEPENDENCY):
    result = db.query(TaskModel).filter(TaskModel.id == task_id).one_or_none()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(result, key, value)
    
    db.commit()
    db.refresh(result)
    return result

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int = Path(..., gt=0), db:Session = DB_DEPENDENCY):
    result = db.query(TaskModel).filter(TaskModel.id == task_id).one_or_none()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    db.delete(result)
    db.commit()
    return {"detail": f"Task with id {task_id} has been deleted successfully"}