from pydantic import BaseModel, UUID4


class CarouselItemBase(BaseModel):
    title: str
    description: str

class CarouselItemFull(CarouselItemBase):
    uuid: UUID4
    image: str

    class Config:
        orm_mode = True
