from stock.database import Base
from sqlalchemy import Boolean, Column, UUID, Integer, String, JSON, Float
from uuid import uuid4

class CarouselItem(Base):

    __tablename__ = "carousel"

    uuid = Column(UUID, primary_key=True, default=uuid4)
    title = Column(String)
    description = Column(String)
    image = Column(String, nullable=True)


class Settings(Base):

    __tablename__ = "settings"

    uuid = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String)
    value = Column(String)
    additional = Column(JSON, nullable=True)

class Products(Base):
    __tablename__ = "products"

    uuid = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String)
    attachments = Column(JSON, nullable=True)
    description = Column(String)
    properties = Column(JSON, nullable=True)
    price = Column(Float)