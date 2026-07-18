from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData(schema="epam")

class Base(DeclarativeBase):
    metadata = metadata 