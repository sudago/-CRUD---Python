from sqlalchemy.orm import Session
import models, schema

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.name == user_name).first()

def create_user(db: Session, user: schema.UserCreate):
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()
     
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()
     
def create_post(db: Session, post: schema.PostCreate, user_id: int):
    db_post = models.Post(**post.model_dump(), writer_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post: schema.Post, updated_post: schema.PostCreate):
    post.title = updated_post.title
    post.body = updated_post.body
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post: schema.Post):
    db.delete(post)
    db.commit()
