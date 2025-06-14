from fastapi import FastAPI
from .routers import example, products, product_reviews, supplier_products, suppliers, enums, orders, order_line_items, shopping_carts, shopping_cart_items

from fastapi.middleware.cors import CORSMiddleware

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

# Include the example.router
# All resources should be built in their own routers file, following that of "example"
app.include_router(example.router)
app.include_router(products.router)
app.include_router(product_reviews.router)
app.include_router(supplier_products.router)
app.include_router(suppliers.router)
app.include_router(enums.router)
app.include_router(orders.router)
app.include_router(order_line_items.router)
app.include_router(shopping_carts.router)
app.include_router(shopping_cart_items.router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}