from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import UserCreate, UserResponse, UserUpdate
from app.dependencies import get_db, Database

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}},
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать пользователя",
    description="Создаёт нового пользователя с указанным email и именем.",
)
def create_user(user: UserCreate, db: Database = Depends(get_db)) -> UserResponse:
    """
    Создать нового пользователя.

    - **email**: уникальный email пользователя
    - **name**: имя пользователя
    - **age**: возраст
    """
    if db.user_exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {user.email} уже зарегистрирован",
        )

    new_user = db.create_user(email=user.email, name=user.name, age=user.age)

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        name=new_user.name,
        age=new_user.age,
        created_at=new_user.created_at,
        is_active=new_user.is_active,
    )


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Получить всех пользователей",
)
def get_users(db: Database = Depends(get_db)) -> list[UserResponse]:
    """Получить список всех пользователей."""
    users = db.get_all_users()
    return [
        UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            age=user.age,
            created_at=user.created_at,
            is_active=user.is_active,
        )
        for user in users
    ]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Получить пользователя по ID",
)
def get_user(user_id: int, db: Database = Depends(get_db)) -> UserResponse:
    """Получить пользователя по его ID."""
    user = db.get_user(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с ID {user_id} не найден",
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        age=user.age,
        created_at=user.created_at,
        is_active=user.is_active,
    )


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Обновить пользователя",
)
def update_user(
    user_id: int, user_update: UserUpdate, db: Database = Depends(get_db)
) -> UserResponse:
    """
    Частичное обновление пользователя.

    Передайте только те поля, которые нужно обновить.
    """
    existing_user = db.get_user(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с ID {user_id} не найден",
        )

    if user_update.email and user_update.email != existing_user.email:
        if db.user_exists(user_update.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {user_update.email} уже зарегистрирован",
            )

    updated_user = db.update_user(
        user_id=user_id,
        email=user_update.email,
        name=user_update.name,
        age=user_update.age,
        is_active=user_update.is_active,
    )

    return UserResponse(
        id=updated_user.id,
        email=updated_user.email,
        name=updated_user.name,
        age=updated_user.age,
        created_at=updated_user.created_at,
        is_active=updated_user.is_active,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя",
)
def delete_user(user_id: int, db: Database = Depends(get_db)):
    """Удалить пользователя по ID."""
    if not db.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с ID {user_id} не найден",
        )

    return None
