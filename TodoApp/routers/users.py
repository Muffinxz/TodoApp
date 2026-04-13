from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from ..models import Users
from typing import Annotated
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .Auth import get_current_user
from passlib.context import CryptContext

router=APIRouter(
    prefix="/users",
    tags=['users']
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()



db_dependency=Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict, Depends(get_current_user)]
bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')


class user_verification(BaseModel):
    password : str
    new_password: str = Field(min_length=6)

class Phonerequest(BaseModel):
    phone_number: str

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user : user_dependency, db: db_dependency):
    if user is None: 
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    found_user = db.query(Users).filter(Users.id==user.get('id')).first()
    if found_user is None:
        raise HTTPException(status_code=404, detail='user not found')
    return found_user


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password ( user: user_dependency, db : db_dependency, userverif : user_verification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()
    if not bcrypt_context.verify(userverif.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Verification failed')
    user_model.hashed_password=bcrypt_context.hash(userverif.new_password)
    db.add(user_model)
    db.commit()

@router.put("/phone_number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phonenumber(user: user_dependency, db: db_dependency,
                          phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()

