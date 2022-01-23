

from shutil import register_unpack_format
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from typing import List

from pydantic import UrlError
from models import User, Role, Gender, UserUpdateRequest

app = FastAPI()

db: List[User]=[
    User(
        id=uuid4(),
        first_name="Victoria",
        last_name="Daniel",
        gender=Gender.female,
        roles=[Role.student]
    ), User(
         id=uuid4(),
        first_name="Andrew",
        last_name="Abe",
        gender=Gender.male,
        roles=[Role.user,Role.admin]
    )]

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/api/v1/users")
async def fetch_Users():
    return db 


@app.post("/api/v1/users")
async def register_Users( user : User):
    db.append(user)
    return {"user" : user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user( user_id: UUID):
    for user in db:
        if user.id==user_id:
            db.remove(user)
            return {"message": f"{user_id} has been deleted"}
    raise HTTPException (status_code=404, detail=f"user with id : {user_id} does not exists")



@app.put("/api/v1/users/{user_id}")
async def update_user( user_update: UserUpdateRequest, user_id: UUID) :
    for user in db:
        if user.id==user_id:
            if user_update.first_name is not None:
                user.first_name=user_update.first_name
            if user_update.last_name is not None:
                user.last_name=user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name=user_update.middle_name
            if user_update.roles is not None:
                user.roles=user_update.roles
            return
        
    
    raise HTTPException (status_code=404, detail=f"user with id : {user_id} does not exists")
