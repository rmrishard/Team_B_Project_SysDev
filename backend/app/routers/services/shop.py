from typing import List, Any
import uuid
from fastapi import APIRouter, HTTPException, Request
from sqlmodel import Session, select, col
from sqlalchemy.exc import IntegrityError

from app import engine
from app.models.shopping_carts import *
from app.utils.orm import ReadItems, UpdateItems
from app.models.services.carts import CartPublic
from .authorize import confirm_session
from ...models.services.carts import CartProductStub, CartShoppingCartItemStub, CartModifyRequest, CartActionEnum
from ...models.shopping_cart_items import ShoppingCartItem
from ...models.shopping_carts import ShoppingCart
from ...models.products import Product

router = APIRouter(
    prefix="/shop",
    tags=["shop"],
    responses={404: {"description": "Not found"}},
)

GUEST_CART_TIMEOUT = 14     # TODO: Number of days to allow a GUEST cart to be active before expiring (set 0 for no limit)
USER_CART_TIMEOUT = 14      # TODO: Number of days to allow a USER cart to be active before expiring (set 0 for no limit)

#Utilize POST for now, but information should be pulled directly from the session
@router.get("/cart/", response_model=Any)
async def get_cart(request: Request):
    shopping_cart_id = None
    products = None

    # Retrieve the Cart
    cart = retrieve_cart(request)
    if cart:
        # Store cart_id in encrypted session to expedite future processing
        shopping_cart_id = str(cart.shopping_cart_id_pk)
        request.session["shopping_cart_id"] = shopping_cart_id
    else:
        raise HTTPException(status_code=404, detail="Failed to retrieve a cart.")

    # Retrieve shopping_cart_items
    cart_items = retrieve_cart_items(shopping_cart_id)

    cart_items = None if not cart_items else cart_items #For consistency set to None (not empty list)

    if cart_items:
        product_ids = map(lambda item: item.product_id_fk, cart_items)
        products = retrieve_cart_products(product_ids)

        #Covert to stubs
        cart_items = map(lambda ci: CartShoppingCartItemStub.from_ShoppingCartItem(ci), cart_items )

    cart = CartPublic.from_ShoppingCart(cart)
    return {"cart":cart,"cart_items":cart_items,"cart_products":products}

@router.post("/cart/modify", response_model=Any)
async def modify_cart(request: Request, cart_request: CartModifyRequest):
    active_session = confirm_session(request.session)

    if active_session:
        # Attempt to retrieve cart_id from session if present
        cart_id = request.session.get("shopping_cart_id", None)

        if cart_id:
            perform_cart_action(cart_id, cart_request)
        else:
            raise HTTPException(status_code=404, detail="Unknown error. Failed to retrieve a cart.")
    else:
        raise HTTPException(status_code=404, detail="Failed to modify items in cart.")


def retrieve_cart(request: Request):
    active_session = confirm_session(request.session)
    cart = None

    if active_session:

        # Attempt to retrieve cart_id from session if present
        cart_id = request.session.get("shopping_cart_id", None)
        cart = ReadItems.with_id(ShoppingCart, cart_id) if cart_id else None

        if cart:
            return cart

        # Fallback to other methods for retrieving shopping cart
        user_id = request.session["credential"].get("user_id", None)
        guest_token = request.session["credential"].get("guest_token", None)

        # Pass both, priority given to user_id
        cart = retrieve_cart_from_db(user_id=user_id,guest_token=guest_token)

        if not cart:
            # Pass both, priority given to user_id
            cart = create_cart(user_id=user_id,guest_token=guest_token)

        if not cart:
            raise HTTPException(status_code=404, detail="Failed to retrieve a new cart")


    return cart

def retrieve_cart_from_db(user_id=None, guest_token=None):
    cart = None

    if not user_id and not guest_token:
        return None

    with Session(engine) as session:
        statement = None

        if user_id:
            statement = select(ShoppingCart).where(ShoppingCart.user_id_fk == user_id)
        elif guest_token:
            statement = select(ShoppingCart).where(ShoppingCart.guest_token == guest_token)

        if statement is not None:
            cart = session.exec(statement).first()
            # ENFORCE EXPIRATION

    return cart

def create_cart(user_id=None, guest_token=None):

    if not user_id and not guest_token:
        return None
    else:
        cart = None
        with Session(engine) as session:
            if user_id:
                cart = ShoppingCart(user_id=user_id)
            elif guest_token:
                cart = ShoppingCart(guest_token=guest_token)

            session.add(cart)
            session.commit()
            session.refresh(cart)

    return cart

def retrieve_cart_items(shopping_cart_id: str):
    if not shopping_cart_id:
        return None

    by_cart_id = lambda sel: sel.where(ShoppingCartItem.shopping_cart_id_fk == shopping_cart_id)
    cart_items = ReadItems.all_with(ShoppingCartItem, by_cart_id)

    return cart_items

def retrieve_cart_products(product_ids: List[str]):
    if not product_ids:
        return None

    in_list = lambda sel: sel.where(col(Product.product_id_pk).in_(product_ids))
    products = ReadItems.all_with(Product, in_list)

    return products


def perform_cart_action(cart_id, cart_request):
    if not cart_id:
        return None
    else:
        with Session(engine) as session:
            statement = select(ShoppingCartItem).where(ShoppingCartItem.shopping_cart_id_fk == cart_id).where(
                ShoppingCartItem.product_id_fk == cart_request.product_id)

            cart_item = session.exec(statement).first()

            if cart_request.action == CartActionEnum.ADD and not cart_item:

                # Only allow non-zero quantities to be committed to DB
                if cart_request.quantity:
                    cart_item = ShoppingCartItem(shopping_cart_id_fk=cart_id,product_id_fk=cart_request.product_id,quantity=cart_request.quantity)
                    session.add(cart_item)

            else:
                if cart_item:
                    if cart_request.action == CartActionEnum.REMOVE or not bool(cart_request.quantity):
                        session.delete(cart_item)
                        cart_item = None
                    elif cart_request.action == CartActionEnum.CHANGE or bool(cart_request.quantity):
                        cart_item.quantity = cart_request.quantity
                        session.add(cart_item)
                else:
                    raise HTTPException(status_code=404, detail="Unknown error. Failed to find requested cart item.")

            # Commit session
            session.commit()

            if cart_item:
                session.refresh(cart_item)

    return cart_item

