from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True
  # rating: Optional[int] = None
  
class PostCreate(PostBase):
  pass

class UserOut(BaseModel):
  id: str
  email: EmailStr
  created_at: datetime
  class Config:
    orm_mode = True

class Post(PostBase):
  id: int
  created_at: datetime
  owners_id: int
  owner: UserOut
  
  class Config:
    orm_mode = True
    
class PostOut(BaseModel):
  Post: Post
  votes: int
  
  class Config:
    orm_mode = True
  
class PostUpdate(BaseModel):
  title: str
  content: str
  published: bool
 
  
# Users
class UserCreate(BaseModel):
  email: EmailStr
  password: str
  
  
class UserLogin(BaseModel):
  email: EmailStr
  password: str
  
class Token(BaseModel):
  access_token: str
  token_type: str
  
class Token_Data(BaseModel):
  id: Optional[str] = None
  
class Vote(BaseModel):
  post_id: int
  dir: conint(le=1)