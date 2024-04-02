from sqlalchemy import Integer, Integer
from src.database.DatabaseContext import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property


class Product(db.Model):

    __tablename__ = "kabum_products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True
    )
    _kabum_product_id: Mapped[int] = mapped_column(
        "kabum_product_id",
        Integer,
        nullable=False,
        unique=True
    )
    _product_name: Mapped[str] = mapped_column(
        "product_name",
        Integer,
        nullable=False
    )
    _product_price: Mapped[int] = mapped_column(
        "product_price",
        Integer,
        nullable=False
    )
    _product_prime_ninja_price: Mapped[int] = mapped_column(
        "product_prime_ninja_price",
        Integer,
        nullable=True
    )
    _product_black_friday_price: Mapped[int] = mapped_column(
        "product_black_friday_price",
        Integer,
        nullable=True
    )
    _product_black_friday_price_with_discount: Mapped[int] = mapped_column(
        "product_black_friday_price_with_discount",
        Integer,
        nullable=True
    )

    @hybrid_property
    def kabum_product_id(self) -> int:
        return self._kabum_product_id

    @kabum_product_id.setter
    def kabum_product_id(self, kabum_product_id: int) -> None:
        self._kabum_product_id = kabum_product_id

    @hybrid_property
    def product_name(self) -> str:
        return self._product_name

    @product_name.setter
    def product_name(self, product_name: str) -> None:
        self._product_name = product_name

    @hybrid_property
    def product_price(self) -> int:
        return self._product_price

    @product_price.setter
    def product_price(self, product_price: int) -> None:
        self._product_price = product_price

    @hybrid_property
    def product_prime_ninja_price(self) -> int:
        return self._product_prime_ninja_price

    @product_prime_ninja_price.setter
    def product_prime_ninja_price(self, product_prime_ninja_price: int) -> None:
        self._product_prime_ninja_price = product_prime_ninja_price

    @hybrid_property
    def product_black_friday_price(self) -> int:
        return self._product_black_friday_price

    @product_black_friday_price.setter
    def product_black_friday_price(self, product_black_friday_price: int) -> None:
        self._product_black_friday_price = product_black_friday_price

    @hybrid_property
    def product_black_friday_price_with_discount(self) -> int:
        return self._product_black_friday_price_with_discount

    @product_black_friday_price_with_discount.setter
    def product_black_friday_price_with_discount(self, product_black_friday_price_with_discount: int) -> None:
        self._product_black_friday_price_with_discount = product_black_friday_price_with_discount
