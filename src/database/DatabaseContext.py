from sqlalchemy import Integer, String
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class DatabaseContext(DeclarativeBase):
    __abstract__ = True


db = SQLAlchemy(model_class=DatabaseContext)