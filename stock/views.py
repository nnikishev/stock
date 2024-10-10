from fastapi import Depends, Request, APIRouter, UploadFile
from fastapi_utils.cbv import cbv
from typing import List

from stock.exceptions import Unauthorized
import logging
import aiofiles

from stock.models import CarouselItem, Settings
from stock.database import asession, engine
from stock.schemas import (
    CarouselItemBase,
    CarouselItemFull,
    SettingBase,
    SettingFull,
)
from sqlalchemy import select, update, delete


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
                result = query_result.scalars().all()
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
                    .values(image=f"http://localhost:8000/static/carousel-images/{file.filename}"))
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
    
    @router.get("/settings/get_by_name/{name}", tags=["settings"], response_model=SettingFull)
    async def get_by_name(self, name):
        async with asession.begin() as session:
            stmt = select(self.model).where(self.model.name==name)
            query_result = await session.execute(stmt)
            instance = query_result.scalars().first()
        return instance
    
    @router.delete("/csettings/{uuid}/", tags=["settings"])
    async def delete_item(self, uuid):
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