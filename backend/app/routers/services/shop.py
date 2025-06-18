from typing import List, Any
import uuid
from fastapi import APIRouter, HTTPException, Request
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from app import engine
from app.models.shopping_carts import *
from app.utils.orm import ReadItems, UpdateItems
from app.models.services.carts import CartPublic

router = APIRouter(
    prefix="/shop",
    tags=["shop"],
    responses={404: {"description": "Not found"}},
)

#Utilize POST for now, but information should be pulled directly from the session
@router.get("/cart/", response_model=Any)
async def retrieve_cart(request: Request):
    request.session["cart"] = {"items": ["Apple","Banana","Carrots"]}

    # items = ReadItems.read(ShoppingCart)
    # if not items:
    #     raise HTTPException(status_code=404, detail="No shopping carts found")
    # return items
    return