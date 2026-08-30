from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.user import User

from app.schemas.user import (

    UserResponse,

    UserUpdate,

    UserRoleUpdate,

)

from app.core.permissions import require_roles

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get(
    "/",
    response_model=list[UserResponse]
)

# Solo un admin puede consultar todos los usuarios.
def get_users(
    db:Session = Depends(get_db),
    current_user:User = Depends(
        require_roles("admin","support")
    )
):
    return db.query(User).all()

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id:int,
    db:Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin","support")
    )
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin","support")
    ),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    update_data = user_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

@router.patch(
    "/{user_id}/role",
    response_model=UserResponse,
)
def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin")
    ),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    allowed_roles = {
        "employee",
        "support",
        "admin",
    }

    if role_data.role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail="Invalid role",
        )

    allowed_categories = {
        "hardware",
        "software",
        "network",
        "access",
        "account",
        "other",
    }

    if role_data.support_category is not None:
        if role_data.support_category not in allowed_categories:
            raise HTTPException(
                status_code=400,
                detail="Invalid support category",
            )

    user.role = role_data.role

    if role_data.role == "support":
        user.support_category = role_data.support_category
    else:
        user.support_category = None

    db.commit()
    db.refresh(user)

    return user

