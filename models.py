from sqlalchemy import Column, TEXT, INT, BIGINT 
from sqlalchemy.ext.declarative import declarative_base 

Base = declarative_base()


class Userinfo(Base): 
    __tablename__ = "UserInfo" 

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True) 
    name = Column(TEXT , nullable=False)
    username = Column(TEXT, nullable=False)
    password = Column(INT,nullable=False) 
    phonenumber = Column(TEXT, nullable=False)
    birth = Column(TEXT, nullable=False) 
    email = Column(TEXT, nullable=False)
   
    
    