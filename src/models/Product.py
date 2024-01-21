from sqlalchemy import Integer, String
from src.database.DatabaseContext import db
from sqlalchemy.orm import Mapped, mapped_column


class Product(db.Model):
    
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True
    )
    id_produto: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True
    )
    produto: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    valor_atual: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    valor_prime_ninja: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    valor_black_friday: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    valor_black_friday_desconto: Mapped[str] = mapped_column(
        String,
        nullable=True
    )