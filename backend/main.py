from typing import Union
from fastapi import FastAPI

from .routers import example, products

app = FastAPI()

# Include the example.router
# All resources should be built in their own routers file, following that of "example"
app.include_router(example.router)
app.include_router(products.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
