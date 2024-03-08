from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
# request를 받고, response를 보내기 위해 pydantic 모델 사용 - Java/Spring의 DTO 역할
# 데이터베이스에 실제 값을 맵핑하기 위해 SQLAlchemy 모델 사용 - Java/Spring의 Entity 역할

class PostBase(BaseModel):
    title: str
    body: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    writer_id: int
    # lazy loading 하지 않고 바로 릴레이션인 users의 값에 접근 가능하도록 설정.
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    posts: List[Post] = []

    class Config:
        from_attributes = True
