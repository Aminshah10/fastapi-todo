from fastapi import APIRouter, Depends
from app.auth.jwt_auth import get_authenticated_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/public")
async def get_public_info():
    return {"message": "This is a public endpoint."}


@router.get("/private")
async def get_private_info(user=Depends(get_authenticated_user)):  # noqa: B008
    return {"message": f"This is a private endpoint. Hello, {user.username}!"}
