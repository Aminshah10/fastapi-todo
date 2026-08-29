from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.jwt_auth import (
    generate_access_token,
    generate_refresh_token,
    save_refresh_token,
    validate_refresh_token,
)
from app.core.database import get_db
from app.users.schemas import RefreshTokenSchema, TokenResponseSchema

router = APIRouter(prefix="/auth", tags=["Authentication"])

DB_DEPENDENCY = Depends(get_db)


@router.post("/refresh")
def get_access_by_refresh_token(
    token: RefreshTokenSchema, db: Session = DB_DEPENDENCY
):
    user_obj, old_token = validate_refresh_token(db, token.refresh_token)

    access_token = generate_access_token(user_obj.id)
    generated_refresh_token, expiration_date = generate_refresh_token(user_obj.id)

    try:
        old_token.revoked = True
        save_refresh_token(
            db=db,
            user_id=user_obj.id,
            refresh_token=generated_refresh_token,
            expiration_date=expiration_date,
        )

        db.commit()
    except Exception:
        db.rollback()
        raise

    return TokenResponseSchema(
        access_token=access_token, refresh_token=generated_refresh_token
    )
