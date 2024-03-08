from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schema
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 게시물 생성
@app.post("/users/{user_name}/posts/", response_model=schema.Post)
def create_post(user_name: str, post: schema.PostCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user_name=user_name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return crud.create_post(db, post=post, user_id=db_user.id)

# 모든 게시물 읽기
@app.get("/posts/", response_model=List[schema.Post])
def read_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)

# 게시물 읽기
@app.get("/posts/{post_id}", response_model=schema.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return db_post

# 게시물 수정
@app.put("/posts/{post_id}", response_model=schema.Post)
def update_post(post_id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return crud.update_post(db, post=db_post, updated_post=updated_post)

# 게시물 삭제
@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    crud.delete_post(db, post=db_post)
    return {"message": "게시글이 삭제되었습니다."}


## 유저 생성
@app.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user_name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 있는 이름입니다.")
    return crud.create_user(db=db, user=user)

## 유저 읽기
@app.get("/users/{user_name}", response_model=schema.User)
def read_user(user_name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user_name=user_name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return db_user

## 모든 유저 읽기
@app.get("/users/", response_model=List[schema.User])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
