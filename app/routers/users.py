from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
  tags=["Users"]  
)

# Users Block
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  
  # hash password
  hashed_password = utils.hash(user.password)
  user.password = hashed_password
  
  new_user = models.User(email=user.email, password=user.password)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

@router.get("/users/{id}", response_model=schemas.UserOut)
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {id} is not the database")
  
  return user