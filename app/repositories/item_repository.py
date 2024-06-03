from typing import List
from app.models.item_model import Item
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class ItemRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["items"]

    async def create_item(self, item: Item) -> Item:
        result = await self.collection.insert_one(item.dict(by_alias=True))
        # item.id = str(result.inserted_id)
        document = await self.collection.find_one({"_id": result.inserted_id})
        return Item(**document)

    async def get_item(self, item_id: str) -> Item:
        document = await self.collection.find_one({"_id": ObjectId(item_id)})
        return Item(**document) if document else None

    async def list_items(self) -> List[Item]:
        items = []
        async for document in self.collection.find():
            items.append(Item(**document))
        return items

    async def update_item(self, item_id: str, item: Item) -> bool:
        result = await self.collection.update_one({"_id": ObjectId(item_id)}, {"$set": item.dict(by_alias=True)})
        return result.modified_count > 0

    async def delete_item(self, item_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0
