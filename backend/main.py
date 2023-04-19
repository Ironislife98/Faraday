from util.keyderivation import derive_auth_key
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import db_interaction
from util.common import load_config
from typing import Annotated


db: db_interaction.DatabaseHandler = db_interaction.DatabaseHandler()

config: dict = load_config()

app: FastAPI = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get('/')
async def root():
    return {"msg": "message"}


@app.post("/register")
async def register(username: str, password: str):
    hashed_password = derive_auth_key(password, config["salt"].encode(config["format"]))
    res = db.create_user(username, hashed_password)
    return {"msg": res}


@app.post("/auth")
async def auth(username: str, password: str):
    hashed_password = derive_auth_key(password, config["salt"].encode(config["format"]))
    res: str = db.login(username, hashed_password)

    # TODO: Add json web token support here
    return {"msg": res}


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordBearer, Depends()]):
    hashed_password = derive_auth_key(form_data.password, config["salt"].encode(config["format"]))
    res: str = db.login(form_data.username, hashed_password)
    return {"access_token": res, "token_type": "bearer"}


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
