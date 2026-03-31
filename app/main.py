from fastapi import FastAPI
from app.api.v1.endpoints import products

app = FastAPI(title="Market Self-Checkout API")

app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])


@app.get("/")
async def root():
    return {"message": "Bem-vindo ao sistema de Autoatendimento!s" }


