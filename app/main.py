from fastapi import FastAPI
from . import models
from .database import engine
from .config import settings
from .routers import posts, users, auth, votes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


# To make alembic migrations do its function
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
  
# while True:
#   try:
#     conn = psycopg2.connect(host="localhost", database="fastapi2", user="postgres", password="marcusaurelius", cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Database connection was successful")
#     break
#   except Exception as error:
#     print("Database connection Failed")
#     print("Error: ", error)
#     time.sleep(5)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
async def root():
  return {"message": "Hello World"}


