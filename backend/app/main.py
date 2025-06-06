from fastapi import FastAPI
from .routers import example, products, product_reviews, supplier_products, suppliers, enums
app = FastAPI(
    root_path="/api/v1",
    version="1",
    openapi_url="/documentation/openapi.json",
    docs_url="/documentation",
    redoc_url=None)

# Include the example.router
# All resources should be built in their own routers file, following that of "example"
app.include_router(example.router)
app.include_router(products.router)
app.include_router(product_reviews.router)
app.include_router(supplier_products.router)
app.include_router(suppliers.router)
app.include_router(enums.router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}