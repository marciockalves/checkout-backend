from fastapi import HTTPException, status
from app.repository.product_repository import ProductRepository

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def get_all_paginated(
        self, 
        page: int, 
        size: int, 
        sort_by: str, 
        order: str
    ):
        
        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A página deve ser maior que zero."
            )


        allowed_sort_columns = ["name", "price", "stock_quantity", "created_at"]
        if sort_by not in allowed_sort_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ordenação por '{sort_by}' não é permitida. Use: {allowed_sort_columns}"
            )

        
        max_page_size = 100
        if size > max_page_size:
            size = max_page_size # "Clamp" o valor em vez de dar erro

        
        return await self.repository.get_all_paginated(
            page=page, 
            size=size, 
            sort_by=sort_by, 
            order=order
        )