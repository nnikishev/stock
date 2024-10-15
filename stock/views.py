from fastapi import Depends, Request, APIRouter, UploadFile
from fastapi_utils.cbv import cbv
from typing import List
from uuid import uuid4

from stock.exceptions import Unauthorized
import logging
import aiofiles

from stock.models import (CarouselItem, Settings, Products, Tag,
    association_table)
from stock.database import asession, engine
from sqlalchemy.orm import selectinload
from stock.schemas import (
    CarouselItemBase,
    CarouselItemFull,
    SettingBase,
    SettingFull,
    ProductsBase,
    ProductsFull,
    TagCreate,
    TagFull
)
from sqlalchemy import select, update, delete
from env import SERVER_HOST

import jwt

router = APIRouter()

logger = logging.getLogger(__name__)

def get_raw(token):
    try:
        raw_jwt = jwt.decode(
                    jwt=token, key=SIGNATURE, algorithms=["HS256"]
                )
    except jwt.exceptions.DecodeError:
        raise Unauthorized(detail="Ошибка расшифровки токена", status_code=401)
    return raw_jwt
    


class CRUDManager:

    model = None
    create_update_schema = None
    auth = None
    lookup_field = "id"

    async def list(self):
        async with asession.begin() as session:
            try:
                stmt = select(self.model)
                query_result = await session.execute(stmt)
                result = query_result.unique().scalars().all()
            except Exception as err:
                logger.error(err)
        return result
    
    async def create(self, item):
        async with asession.begin() as session:
            item_mapping = item.model_dump()
            new = self.model(**item_mapping)
            session.add(new)
            await session.commit()
            # await session.refresh(new)
        return new
    
    async def get(self, uuid):
        async with asession.begin() as session:
            stmt = select(self.model).where(self.model.uuid==uuid)
            query_result = await session.execute(stmt)
            instance = query_result.scalars().first()
        return instance
    
    async def delete(self, uuid):
        async with asession.begin() as session:
            stmt = delete(self.model).where(self.model.uuid==uuid)
            await session.execute(stmt)
        return None

@cbv(router)
class CarouselAPI(CRUDManager):

    model = CarouselItem
    create_update_schema = CarouselItemBase

    @router.get("/carousel-items/", tags=["carousel"], response_model=List[CarouselItemFull])
    async def get_list(self):
        return await super().list()
    
    @router.post("/carousel-item/", tags=["carousel"], response_model=CarouselItemFull)
    async def create_item(self, item: create_update_schema):
        return await super().create(item)
    
    @router.put("/carousel-item/{uuid}/upload-image/", tags=["carousel"], response_model=CarouselItemFull)
    async def upload_image(self, uuid, file: UploadFile):
        async with aiofiles.open(f"static/carousel-images/{file.filename}", 'wb+') as out_file:
            content = await file.read() 
            await out_file.write(content)

        async with asession.begin() as session:
            stmt = (update(self.model)
                    .where(self.model.uuid==uuid)
                    .values(image=f"http://{SERVER_HOST}:8000/static/carousel-images/{file.filename}"))
            await session.execute(stmt)
            stmt = select(self.model).where(self.model.uuid==uuid)
            query_result = await session.execute(stmt)
            result = query_result.scalars().first()
        return result
    
    @router.delete("/carousel-item/{uuid}/", tags=["carousel"])
    async def delete_item(self, uuid):
        return await super().delete(uuid)

@cbv(router)
class SettingsAPI(CRUDManager):
    model = Settings
    create_update_schema = SettingBase

    @router.get("/settings/", tags=["settings"], response_model=List[SettingFull])
    async def get_list(self):
        return await super().list()
    
    @router.post("/settings/", tags=["settings"], response_model=SettingFull)
    async def create_item(self, item: create_update_schema):
        return await super().create(item)
    
    @router.get("/settings/{uuid}/", tags=["settings"], response_model=SettingFull)
    async def get(self, uuid):
        return await super().get(uuid)
    
    @router.get("/settings/get_by_name/{name}/", tags=["settings"], response_model=SettingFull)
    async def get_by_name(self, name):
        async with asession.begin() as session:
            stmt = select(self.model).where(self.model.name==name)
            query_result = await session.execute(stmt)
            instance = query_result.scalars().first()
        return instance
    
    @router.delete("/settings/{uuid}/", tags=["settings"])
    async def delete_item(self, uuid):
        return await super().delete(uuid)
    
@cbv(router)
class ProductsAPI(CRUDManager):
    model = Products
    create_update_schema = ProductsBase

    @router.get("/products/", tags=["products"], response_model=List[ProductsFull])
    async def get_products(self):
        return await super().list()
    
    @router.post('/products/', tags=["products"], response_model=ProductsFull)
    async def create_products(self, item: create_update_schema):
        return await super().create(item)

    @router.get("/product/{uuid}/", tags=["products"]) 
    async def get(self, uuid):
        return await super().get(uuid)
    

    @router.put("/product/{uuid}/add-product-images/", tags=["products"]) # response_model=ProductsBase
    async def put_product_images(self, uuid, files: List[UploadFile]):
        result = []
        for file in files:
            async with aiofiles.open(f"static/products-images/{file.filename}", 'wb+') as out_file:
                content = await file.read() 
                await out_file.write(content)

            result.append(f"http://{SERVER_HOST}:8000/static/products-images/{file.filename}")

        async with asession.begin() as session:
            stmt = (update(self.model)
                    .where(self.model.uuid==uuid)
                    .values(attachments=result))
            await session.execute(stmt)
            stmt = select(self.model).where(self.model.uuid==uuid)
            query_result = await session.execute(stmt)
            response = query_result.scalars().first()

        return response
    
    @router.put("/product/{uuid}/set-tag/{tag_uuid}", tags=["products"])
    async def set_tag(self, uuid, tag_uuid):
        async with asession.begin() as session:
            product = await session.execute(
                select(self.model).where(self.model.uuid == uuid)
            )
            await session.execute(association_table.insert().values(
                uuid=uuid4(), product_uuid=uuid, tag_uuid=tag_uuid))
            await session.flush()
            await session.commit()
        return product.scalars().first()

    
    @router.delete("/product/{uuid}/", tags=["products"])
    async def delete_product(self, uuid):
        return await super().delete(uuid)


@cbv(router)
class TagAPI(CRUDManager):

    model = Tag
    create_update_schema = TagCreate

    @router.get("/tags/", tags=["tags"], response_model=List[TagFull])
    async def get_products(self):
        return await super().list()
    
    @router.post('/tags/', tags=["tags"], response_model=TagFull)
    async def create_products(self, item: create_update_schema):
        return await super().create(item)

    @router.get("/tags/{uuid}/", tags=["tags"], response_model=TagFull) 
    async def get(self, uuid):
        return await super().get(uuid)
    
    @router.delete("/tags/{uuid}/", tags=["tags"])
    async def delete_product(self, uuid):
        return await super().delete(uuid)
    


# @app.get("/secret/")
# def get_secret(request: Request):
#     try:
#         auth_token = request.headers["Auth"]
#     except KeyError:
#         raise Unauthorized(detail="Отсутствует токен авторизации", status_code=401)
#     credentials = get_raw(auth_token)
#     if not "view_api" in credentials["claims"]["permissions"]:
#         raise Unauthorized(
#             detail=f"Отсутствуют привилегии для просмотра API для {credentials['username']}", 
#             status_code=401
#             )
#     return {"status": f"Доступ для пользователя {credentials['username']} разрешен"}