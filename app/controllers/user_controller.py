from fastapi import APIRouter, HTTPException
from app.config import database

router = APIRouter()

@router.get("/test-connection")
async def test_connection():
    try:
        collections = await database.list_collection_names()
        return {"status": "success", "collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users")
async def get_users():
    return {"message": "Get all users"}





