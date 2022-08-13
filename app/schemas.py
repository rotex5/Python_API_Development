from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class PostBase(BaseModel):
    #this schema defines the kind of data the api accepts
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None


class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    #NOTE: this class was initially below UserCreate, but was moved here because its class
    #name was called in PostResponse. So it needs to be define before a place where it is called.
    #Because python reads from top to bottom
    id : int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    #Note: title, content and published were inherited too.They will be displayed along side id & created_at.
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int      #Note: its was labled "votes" because that was the column name asigned in the .join query of the result variable in post.py

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Votes(BaseModel):
    post_id: int
    dir: conint(le=1)  #direction. 0 reps "Not Voted" while 1 reps "Voted"
