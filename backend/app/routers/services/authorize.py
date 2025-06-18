from typing import List, Any, Annotated
import uuid
import json

from fastapi import APIRouter, HTTPException, Request, Form, Response
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app import engine
from app.models.shopping_carts import *
from app.models.services.credentials import Credential
from app.models.users import hash_password, User, UserPublicRetrieve

router = APIRouter(
    prefix="/auth",
    tags=["authorization"],
    responses={404: {"description": "Not found"}},
)

#Utilize POST for now, but information should be pulled directly from the session
@router.post("/login", response_model=Any)
async def login(response: Response, request: Request, username: Annotated[str, Form()], password: Annotated[str, Form()]):

    hashed_password = hash_password(password)
    with Session(engine) as session:
        statement = select(User).where(User.username == username,User.password == hashed_password)
        user = session.exec(statement).first()

        if user:
            credential = Credential(user_id=user.user_id_pk,username=username,role=user.getUserRole())
            request.session["credential"] = credential.model_dump(mode='json')
            response.status_code = HTTP_200_OK

            plain_user = {"first_name": user.first_name, "last_name": user.last_name, "id": str(user.user_id_pk)}

            response.set_cookie(key="store_user", value=json.dumps(plain_user))
        else:
            if not request.session.get("credential", None):
                credential = Credential(user_id=None, username=None, role=None)
                request.session["credential"] = credential.model_dump(mode='json')

            response.status_code = HTTP_401_UNAUTHORIZED

    return

@router.post("/logout", response_model=Any)
async def logout(request: Request, response: Response):
    guest_token = request.session["credential"]["username"]
    request.session.clear()
    response.delete_cookie(key="store_user")

    return "Bye!"


@router.post("/whoami", response_model=Optional[UserPublicRetrieve])
def retrieve_user_info(request: Request, response: Response):
    if request.session.get("credential", None):
        user_id = request.session["credential"]["user_id"]
        if user_id:
            with Session(engine) as session:
                user = session.get(User,user_id)

            return user

    return None