from pydantic import BaseModel, UUID4
from datetime import datetime

class FeedbackCreate(BaseModel):
    fio: str
    email: str
    phone: str
    message: str

class FeedbackFull(FeedbackCreate):
    uuid: UUID4
    created_at: datetime = None

class TagCreate(BaseModel):
    title: str

class TagFull(TagCreate):
    uuid: UUID4

    class Config:
        orm_mode = True

class CarouselItemBase(BaseModel):
    title: str
    description: str

class CarouselItemFull(CarouselItemBase):
    uuid: UUID4
    image: str | None = None

    class Config:
        orm_mode = True

class SettingBase(BaseModel):
    name: str
    value: str
    additional: dict | None = None

class SettingFull(SettingBase):
    uuid: UUID4

    class Config:
        orm_mode = True

class ProductsBase(BaseModel):
    uuid: UUID4 | None = None
    name: str
    description: str
    properties: dict | None = None
    price: float

class ProductsFull(ProductsBase):
    uuid: UUID4
    attachments: list | None = None
    tags: list[TagFull] | None = None

    class Config:
        orm_mode = True