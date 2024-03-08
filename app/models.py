from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, text
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__  = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), unique=True, nullable=False)
    # 연관관계 설정 one to many
    posts = relationship("Post", back_populates="writer")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(20), nullable=False)
    body = Column(String(1000))
    # 처음 데이터 삽입 시 default로 생성일자 생성.
    created_at = Column(DateTime(timezone=True), default=text("datetime('now','localtime')"))
    # 데이터가 수정 될 때 자동으로 수정일자 업데이트
    modified_at = Column(DateTime(timezone=True), onupdate=text("datetime('now','localtime')"))
    # 자식 테이블이 부모 테이블을 참조.
    writer_id = Column(Integer, ForeignKey("users.id"))
    # 연관관계 설정 
    writer = relationship("User", back_populates="posts")
