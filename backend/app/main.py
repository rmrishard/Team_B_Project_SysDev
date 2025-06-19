from fastapi import FastAPI, Request
from .routers import example, products, product_reviews, supplier_products, suppliers, enums, orders, order_line_items, \
    shopping_carts, shopping_cart_items, users

from .routers.services import shop, authorize

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(
    root_path="/api/v1",
    version="1",
    openapi_url="/documentation/openapi.json",
    docs_url="/documentation",
    redoc_url=None)

# Setup origins that may be triggered by local testing
origins = [
    "http://localhost:8777",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="9kTqAH54CmOTdH208Jg04npHb4zB3LMv/CcSqNinHvo",
    same_site='strict',
    https_only=False,
    http_only=False
)

# All resources should be built in their own routers file
app.include_router(products.router)
app.include_router(product_reviews.router)
app.include_router(supplier_products.router)
app.include_router(suppliers.router)
app.include_router(enums.router)
app.include_router(orders.router)
app.include_router(order_line_items.router)
app.include_router(shopping_carts.router)
app.include_router(shopping_cart_items.router)
app.include_router(users.router)

# Routers for complex services
app.include_router(shop.router)

app.include_router(authorize.router)
@app.get("/")
def read_root():
    return {"message": "Hello wide world, waiting to service requests!"}

# For heartbeat/is-alive checks
@app.get("/ping")
def ping():
    return {"ping":"pong"}