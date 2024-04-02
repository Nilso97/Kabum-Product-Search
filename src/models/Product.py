from sqlalchemy import Integer, Integer
from src.database.DatabaseContext import db
from sqlalchemy.orm import Mapped, mapped_column


class Product(db.Model):

    __tablename__ = "kabum_products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True
    )
    kabum_product_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True
    )
    product_name: Mapped[str] = mapped_column(
        Integer,
        nullable=False
    )
    product_price: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    product_prime_ninja_price: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
    product_black_friday_price: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
    product_black_friday_price_with_discount: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
