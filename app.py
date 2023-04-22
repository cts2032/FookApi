from fastapi import FastAPI, Depends, Path, HTTPException, File, UploadFile 
from pydantic import BaseModel 
from database import engineconn 
from models import Userinfo
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from fastapi.middleware.cors import CORSMiddleware 

import boto3 

app = FastAPI() 

engine = engineconn() 
session = engine.sessionmaker()

origins = [
    "http://localhost",
    "http://localhost:3000"
    
]


app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

pwd_content = CryptContext(schemes=["bcrypt"],deprecated="auto")

class UserCreate(BaseModel) : 
    username : str
    password : str
    phonenumber : str
    birth : str
    email : str

class User(UserCreate) :
    name : str   
    class Config :
        orm_mode = True   
   
   
def get_db():  # 호출이 되면 db에 세션을 붙임 , yield (return과 유사하나 결과값을 준 후 메모리에 들고 있음.) 
    try:       
        db = session
        yield db
        
    finally : 
        db.close() 
        
@app.post("/regist/" ,tags=['login'])
async def create_user(user : User , db : session = Depends(get_db)):
    if db.query(exists().where(Userinfo.username == user.username)).scalar():
        raise HTTPException(status_code=400 , detail="이미 존재하는 아이디입니다.")
    hashed_password = pwd_content.hash(user.password)
    db_user = Userinfo(username = user.username , password = hashed_password   , phonenumber = user.phonenumber , birth = user.birth , email = user.email, name = user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"username": db_user.username}
