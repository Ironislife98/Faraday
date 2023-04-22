from util.keyderivation import derive_auth_key
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import db_interaction
from util.common import load_config
from typing import Annotated
from models import User, VaultUpdate


db: db_interaction.DatabaseHandler = db_interaction.DatabaseHandler()

config: dict = load_config()

app: FastAPI = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get('/')
async def root():
    return {"msg": "message"}


@app.post("/register")
async def register(user: User):
    hashed_password = derive_auth_key(user.password, config["salt"].encode(config["format"]))
    res = db.create_user(user.username, hashed_password)
    db.create_vault(user.username)
    return {"msg": res}


@app.post("/auth")
async def login(user: User):
    hashed_password = derive_auth_key(user.password, config["salt"].encode(config["format"]))
    res: str = db.login(user.username, hashed_password)

    base64_vault: str = db.get_vault(user.username)
    return {
        "msg": res,
        "vault": base64_vault
        }


@app.post("/vault")
async def update_vault(user: VaultUpdate):
    hashed_password = derive_auth_key(user.password, config["salt"].encode(config["format"]))
    res: str = db.login(user.username, hashed_password)
    db.update_vault(user.username, user.vault)
    return {"msg": "Successful"}