





from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.user import User

from app.schemas.user import (

    UserCreate,

    UserResponse,

    Token,

);

from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (

    hash_password,

    verify_password,

    create_access_token,

    ACCESS_TOKEN_EXPIRE_MINUTES,

)

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user



@router.post(
    "/register",
    response_model=UserResponse
)

def register(
    user_data:UserCreate,
    db:Session = Depends(get_db)
):

        existing_user = (
            db.query(User)
            .filter(User.email == user_data.email)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registrered"
            )
        user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hash_password(
                user_data.password
            ),

        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user



@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        ##  OAuth2 espera un campo llamado username. 
        ## Pero podemos meter el email dentro de username:
        .filter(User.email == form_data.username)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        form_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role,
        },
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }