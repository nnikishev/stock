from stock.database import Base
from sqlalchemy import (
    ForeignKey,
    Boolean, 
    Column, 
    UUID, 
    Integer, 
    String, 
    JSON, 
    Float, 
    Table
)
from uuid import uuid4
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from typing import List
from uuid import UUID as UUID4


association_table = Table(
    "product_tag",
    Base.metadata,
    Column("uuid", UUID, primary_key=True, default=uuid4),
    Column("tag_uuid", ForeignKey("tag.uuid")),
    Column("product_uuid", ForeignKey("products.uuid")),
)

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

    uuid: Mapped[UUID4] = mapped_column(primary_key=True, default=uuid4)
    name = Column(String)
    attachments = Column(JSON, nullable=True)
    description = Column(String)
    properties = Column(JSON, nullable=True)
    price = Column(Float)
    tags: Mapped[List["Tag"]] = relationship(
        secondary=association_table, back_populates="products", lazy="joined"
    )


class Tag(Base):

    __tablename__ = "tag"

    uuid: Mapped[UUID4] = mapped_column(primary_key=True, default=uuid4)
    title = Column(String)
    products:  Mapped[List["Products"]] = relationship(
        secondary=association_table, back_populates="tags", lazy="joined"
    )
