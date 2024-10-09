from stock.database import Base
from sqlalchemy import Boolean, Column, UUID, Integer, String
from uuid import uuid4

class CarouselItem(Base):

    __tablename__ = "carousel"

    uuid = Column(UUID, primary_key=True, default=uuid4)
    title = Column(String)
    description = Column(String)
    image = Column(String, nullable=True)