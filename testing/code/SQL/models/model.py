from sqlalchemy import Column, Integer, DateTime, SmallInteger, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class AppUsers(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(16), nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    access = Column(SmallInteger, nullable=True)
    active = Column(SmallInteger, nullable=True)
    start_active_time = Column(DateTime, nullable=True)

