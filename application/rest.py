from fastapi import FastAPI, status, Depends, HTTPException
from typing import Annotated
from security import auth

#import common
from fastapi.middleware.cors import CORSMiddleware
#from database import engine

app = FastAPI()
app.include_router(auth.router)
#app.include_router(common.router)

@app.get("/")
async def saludar():
    return {'hola':'mundo'}



