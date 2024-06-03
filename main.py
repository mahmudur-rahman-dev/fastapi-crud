from typing import List
from uuid import uuid4, UUID

from fastapi import FastAPI

from models import User, Role, Gender

app = FastAPI()

db: List[User] = [
    User(id=UUID("6edecbe5-ce3a-44a8-adb5-1acafdc758dc"),
         first_name="John",
         last_name="Ahmed",
         gender=Gender.female,
         roles=[Role.student]
         ),
    User(id=UUID("5c5737a8-f170-41cf-a435-6ac0ce76ff56"),
         first_name="Alex",
         last_name="Jones",
         gender=Gender.male,
         roles=[Role.admin, Role.user]
         )
]


@app.get("/")
def root():
    return {"message": "Hello"}


@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.post("/api/v1/users")
async def create_user(user: User):
    db.append(user)
    return {"id": user.id}
