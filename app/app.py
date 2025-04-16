from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from config import settings

class Friend(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    company: str | None = Field(default=None, index=True)
    yearMet: int | None = Field(default=None, index=True)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/friends/", response_model=Friend)
def create_friend(friend: Friend):
    with Session(engine) as session:
        session.add(friend)
        session.commit()
        session.refresh(friend)
        return friend

@app.get("/friends/", response_model=list[Friend])
def read_friends(skip: int = 0, limit: int = 10):
    with Session(engine) as session:
        friends = session.exec(select(Friend).offset(skip).limit(limit)).all()
        return friends

