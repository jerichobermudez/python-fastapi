from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, nullable = False)
    firstname = Column(String, nullable = False, unique = False)
    lastname = Column(String, nullable = False, unique = False)
    username = Column(String, nullable = False, unique = True)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    token = Column(String, nullable = True)
    created_at= Column(
        TIMESTAMP(timezone = True),
        nullable = True,
        server_default = text('now()')
    )
