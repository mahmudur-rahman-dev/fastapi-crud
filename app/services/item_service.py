from typing import List
from app.models.item_model import Item
from app.repositories.item_repository import ItemRepository
from app.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from app.schemas.item_schema import ItemCreateSchema, ItemResponseSchema

class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    async def create_item(self, item: ItemCreateSchema) -> ItemResponseSchema:
        item_model = Item(**item.dict())
        created_item = await self.repository.create_item(item_model)
        return ItemResponseSchema(**created_item.dict())

    async def get_item(self, item_id: str) -> ItemResponseSchema | None:
        item = await self.repository.get_item(item_id)
        if item is None:
            return None
        return ItemResponseSchema(**item.dict())

    async def list_items(self) -> List[ItemResponseSchema]:
        items = await self.repository.list_items()
        return [ItemResponseSchema(**item.dict()) for item in items]

    async def update_item(self, item_id: str, item: ItemCreateSchema) -> bool:
        item_model = Item(**item.dict())
        return await self.repository.update_item(item_id, item_model)

    async def delete_item(self, item_id: str) -> bool:
        return await self.repository.delete_item(item_id)

def get_item_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> ItemService:
    repository = ItemRepository(db)
    return ItemService(repository)
