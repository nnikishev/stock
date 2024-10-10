from pydantic import BaseModel, UUID4


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