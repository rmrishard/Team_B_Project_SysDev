from typing import List
import uuid
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session
from app import engine
from .mocking.users import fake_users as mock_items
from ..models.users import *
from app.utils.orm import ReadItems, UpdateItems

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[UserPublicRetrieve])
async def read_items(offset: int = 0, limit: int = Query(default=20, le=100)):
    select_modifier = lambda sel: sel.offset(offset).limit(limit)
    items = ReadItems.read(User, modifier_fn=select_modifier)

    if not items:
        raise HTTPException(status_code=404, detail="No users found")

    return items

@router.get("/{item_id}", response_model=UserPublicRetrieve)
async def read_item(item_id: uuid.UUID):
    item = ReadItems.with_id(User, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="User not found")

    return item

@router.patch("/{item_id}", response_model=UserPublicRetrieve)
def update_item(item_id: uuid.UUID, item: UserUpdate):
    updated_item = UpdateItems.with_id(User, item, item_id)
    return updated_item

@router.post("/upload/", response_model=List[UserPublicRetrieve])
def create_items(users: List[UserCreate]):
    with Session(engine) as session:
        for user in users:
            user_data = user.model_dump(exclude_unset=True)
            valid_item = User.model_validate(user_data)
            session.add(valid_item)
        session.commit()

    return users
