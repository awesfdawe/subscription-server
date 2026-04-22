from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from src.config import get_settings
from src.auth.dependencies import get_current_admin
from src.database import get_session
from src.models import Users
from src.users.schemas import UserCreateRequest, UserUpdateRequest

settings = get_settings()

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Users)
def create(
    user_data: UserCreateRequest, admin: int = Depends(get_current_admin), session: Session = Depends(get_session)
):
    db_user = Users(**user_data.model_dump())

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.patch("/{user_id}", response_model=Users)
def update(
    user_id: int,
    user_data: UserUpdateRequest,
    admin: int = Depends(get_current_admin),
    session: Session = Depends(get_session),
):
    db_user = session.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    update_data = user_data.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(update_data)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id: int, admin: int = Depends(get_current_admin), session: Session = Depends(get_session)):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    session.delete(user)
    session.commit()
    return None


@router.get("/", response_model=Page[Users])
def get_users(admin: int = Depends(get_current_admin), session: Session = Depends(get_session)):
    query = select(Users).order_by(Users.id)
    return paginate(session, query)


add_pagination(router)
