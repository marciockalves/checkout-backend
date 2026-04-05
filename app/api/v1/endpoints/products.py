from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product_schema import ProductRead, ProductUpdate
from app.repository.product_repository import ProductRepository
from app.db.session import get_db
from app.services.storage_service import StorageService


router =APIRouter()

@router.post("/", response_model=ProductRead)
async def create_product(
    name: str = Form(...),
    barcode: str = Form(...),
    price: float = Form(...),
    stock_quantity: int =  Form(...),
    file: UploadFile = File(...),
    db: AssertionError = Depends(get_db)
    ):
    repo = ProductRepository(db)
    storage = StorageService()

    existing = await repo.get_by_barcode(barcode)

    if existing:
        raise HTTPException(status_code=400, detail= "Barcode already registred")
    
    image_url = await storage.upload_image(file)

    product_data = {
        "name": name,
        "barcode": barcode,
        "price": price,
        "stock_quantity": stock_quantity,
        "image_url": image_url
    }


    return await repo.create(product_data)

@router.get("/{barcode}", response_model=ProductRead)
async def get_product(barcode: str, db:AsyncSession= Depends(get_db)):
    repo= ProductRepository(db)
    product = await repo.get_by_barcode(barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return product

@router.put("/{barcode}", response_model=ProductUpdate)
async def update_produtct(barcode: str, 
                          payload: ProductUpdate, 
                          db: AsyncSession = Depends(get_db)):

    repo = ProductRepository(db)
    updated = await repo.update_by_barcode(barcode, payload)

    print(f"DEBUG: O que o repositório retornou? {updated}")

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail=f"Produto {barcode} não encontrado"
        )

    return updated