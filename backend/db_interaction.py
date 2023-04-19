import sqlalchemy.exc
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from util.common import load_config
from cryptography.hazmat.primitives import constant_time
from fastapi import HTTPException

config: dict = load_config()

# Must be at top of file before classes or anything is loaded
# Prevent some error, I forget
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


# Probably not a good idea to load more than one instance of DatabaseHandler
class DatabaseHandler:
    @staticmethod
    def create_user(username: str, password: str) -> str:
        try:
            user: User = User(username=username, password=password)
            session.rollback()
            session.add(user)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=400, detail="User already exists")
        return "Added User Successfully!"

    @staticmethod
    def login(username: str, password: str) -> str:
        try:
            cursor = session.query(User).filter(User.username == username)
            for user in cursor:
                db_password = user.password
                print(db_password)
            # This function helps prevent against timing attacks, O(n)
            # Attacker does not know how long the data is, or how long it takes to perform the operation
            # Read more: https://codahale.com/a-lesson-in-timing-attacks/
            if constant_time.bytes_eq(password.encode(config["format"]), db_password.encode(config["format"])):
                # The reference of db_password suggests UnBoundLocalError, this is fine it is how we detect no account
                return "Successfully authenticated!"
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        except UnboundLocalError:       # No user found
            raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    
# Sqlalchemy boilerplate
# Generating sqlalchemy stuff
engine = create_engine(config["DATABASE_URL"], echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
