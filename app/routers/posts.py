from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
  tags=["Posts"]
)
# get posts
# @router.get("/posts", response_model=List[schemas.Post])
@router.get("/posts", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_data)):
  posts = db.query(models.Post).filter(models.Post.owners_id == current_user.id).all()
  
  results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
  print(results)
  return results

# get posts by id
@router.get("/posts/{id}", response_model=schemas.PostOut)
async def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_data)):
  post = db.query(models.Post).filter(models.Post.id == id).first()
  post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} was not found")
  return post

#  create posts
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_data)):
  new_post = models.Post(owners_id=current_user.id, title=post.title, content=post.content, published=post.published)
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

#  update posts
@router.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_data)):
  
  query_post = db.query(models.Post).filter(models.Post.id == id)
  obj = query_post.first()
  if obj == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  
  if obj.owners_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail=f"Not an authorized user")
  
  query_post.update(post.dict(), synchronize_session=False)
  return query_post.first()

# delete posts
@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_data)):
  post_query = db.query(models.Post).filter(models.Post.id == id)
  
  post = post_query.first()
  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  
  if post.owners_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not an authorized user")
  
  post_query.delete(synchronize_session=False)
  db.commit()
  
  return Response(status_code=status.HTTP_204_NO_CONTENT)
