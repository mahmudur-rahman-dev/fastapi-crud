from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.item_schema import ItemCreateSchema, ItemResponseSchema
from app.services.item_service import ItemService, get_item_service

router = APIRouter()

@router.post("/", response_model=ItemResponseSchema)
async def create_item(item: ItemCreateSchema, service: ItemService = Depends(get_item_service)):
    try:
        return await service.create_item(item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{item_id}", response_model=ItemResponseSchema)
async def get_item(item_id: str, service: ItemService = Depends(get_item_service)):
    item = await service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/", response_model=List[ItemResponseSchema])
async def list_items(service: ItemService = Depends(get_item_service)):
    try:
        return await service.list_items()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{item_id}", response_model=bool)
async def update_item(item_id: str, item: ItemCreateSchema, service: ItemService = Depends(get_item_service)):
    try:
        success = await service.update_item(item_id, item)
        if not success:
            raise HTTPException(status_code=404, detail="Item not found")
        return success
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{item_id}", response_model=bool)
async def delete_item(item_id: str, service: ItemService = Depends(get_item_service)):
    try:
        success = await service.delete_item(item_id)
        if not success:
            raise HTTPException(status_code=404, detail="Item not found")
        return success
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))