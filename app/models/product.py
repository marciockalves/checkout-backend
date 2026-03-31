from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Numeric, Integer
import uuid

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__="products"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]= mapped_column(String(100), nullable=False)
    barcode: Mapped[str]= mapped_column(String(50), unique=True, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
