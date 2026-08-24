from fastapi import APIRouter

router = APIRouter(tags=["tasks"])

@router.get("/tasks")
def retrieve_all_tasks():
    return []

@router.get("/tasks/{task_id}")
def retrieve_task_detail(task_id : int):
    return []