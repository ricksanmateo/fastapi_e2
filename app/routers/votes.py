from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2, models

router = APIRouter(
  tags=["Votes"]
)

@router.post("/votes", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_data)):
  post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  
  vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
  found_vote = vote_query.first()
  
  if vote.dir == 1:
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    new_vote = models.Votes(post_id = vote.post_id, user_id=current_user.id)
    db.add(new_vote)
    db.commit()
    return {"Message":"successfully added vote"}
  else:
    if not found_vote:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    vote_query.delete(synchronize_session=False)
    db.commit()
    
    return {"Message":"successfully deleted vote"}