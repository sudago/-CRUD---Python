from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 현재 폴더에 있는 sql_app.db 파일을 열어 sqlite 데이터베이스에 connecting 한다.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    # sqlite는 스레드 통신이 불가능하기 때문에 옵션을 붙여 스레드가 하나만 실행되게 만들어준다.
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 데이터베이스 세션
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 이 클래스를 상속 받은 클래스들을 자동으로 데이터베이스 테이블을 매핑시켜줄 수 있다.
Base = declarative_base()
