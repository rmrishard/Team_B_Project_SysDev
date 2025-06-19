from typing import List, Any, Annotated
import uuid
import json

from fastapi import APIRouter, HTTPException, Request, Form, Response
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app import engine
from app.models.shopping_carts import *
from app.models.services.credentials import Credential, LoginCredential
from app.models.users import hash_password, User, UserPublicRetrieve

router = APIRouter(
    prefix="/auth",
    tags=["authorization"],
    responses={404: {"description": "Not found"}},
)

#Confirm session or create a new one if absent
def confirm_session(session, credential: Optional[Credential] = None) -> bool:
    valid_credential = False

    if session.get("credential", None):
        # verify credential is still activate   TODO: ADD INTERNAL EXPIRATION

        # Does the credential have a user_id and/or a guest_token to identify the user on the site?
        valid_credential = bool(session["credential"].get("user_id", None) or session["credential"].get("guest_token", None))
    else:
        if credential:
            session["credential"] = credential.model_dump(mode='json')
        else:
            credential = Credential(user_id=None, username=None, role=None)
            session["credential"] = credential.model_dump(mode='json')

        valid_credential = True  # Credential created

    #do further invalidation if necessary to force re-login or recreation of session
    return valid_credential

#Process login helper function
async def process_login(request, response, username, password ):
    hashed_password = hash_password(password)
    with Session(engine) as session:
        statement = select(User).where(User.username == username, User.password == hashed_password)
        user = session.exec(statement).first()

        if user:
            credential = Credential(user_id=user.user_id_pk, username=username, role=user.getUserRole())
            confirm_session(request.session, credential)

            # Set clear-text information
            plain_user = {"first_name": user.first_name, "last_name": user.last_name, "id": str(user.user_id_pk)}
            response.set_cookie(key="store_user", value=json.dumps(plain_user))
            response.status_code = HTTP_200_OK
        else:
            confirm_session(request.session, None)
            response.status_code = HTTP_401_UNAUTHORIZED


#Expect JSON
@router.post("/login/json")
async def login(response: Response, request: Request, login_request: LoginCredential ):
    if login_request.username and login_request.password:
        await process_login(request, response, login_request.username, login_request.password)


#Utilize POST
@router.post("/login", response_model=Any)
async def login(response: Response, request: Request, username: Annotated[str, Form()], password: Annotated[str, Form()]):

    await process_login(request, response, username, password)

    return

@router.post("/logout", response_model=Any)
async def logout(request: Request, response: Response):
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

# For taking a look at encrypted session data, use only in debugging on local
# @router.get("/debug")
# def debug_dump(request: Request, response: Response):
#     return request.session