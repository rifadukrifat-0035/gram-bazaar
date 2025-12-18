# backend/app/crud/crud_product.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.product import Product
from app.schemas.product import ProductCreate

async def create_product(db: AsyncSession, *, product_in: ProductCreate) -> Product:
    """
    Creates a new product in the database.
    This function is fully asynchronous and type-hinted for clarity.
    """
    db_product = Product(**product_in.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def get_products(db: AsyncSession, *, skip: int = 0, limit: int = 100) -> list[Product]:
    """
    Retrieves a list of products from the database asynchronously.
    Uses modern `select` statement for better performance and readability.
    """
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return list(result.scalars().all()) # Ensure result is a list
