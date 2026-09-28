from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User, UserRole, UserStatus
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
)
from app.schemas.user import UserLogin, UserRegister


def register_user(
    db: Session,
    user_data: UserRegister
) -> User:

    existing_user = get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = hash_password(
        user_data.password
    )

    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password,
        role=UserRole.CUSTOMER,
        status=UserStatus.ACTIVE,
    )

    return create_user(db, user)


def login_user(
    db: Session,
    user_data: UserLogin
) -> str:

    user = get_user_by_email(
        db,
        user_data.email
    )

    if not user:
        raise ValueError("Invalid email or password")

    if not verify_password(
        user_data.password,
        user.password_hash
    ):
        raise ValueError("Invalid email or password")

    if user.status != UserStatus.ACTIVE:
        raise ValueError("User account is inactive")

    access_token = create_access_token(
        user_id=user.id,
        role=user.role.value
    )

    return access_token