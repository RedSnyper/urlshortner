from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router, redirect
from app.db import Base ,engine
app = FastAPI()

app.include_router(router, prefix='/api')
app.include_router(redirect)


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"], 
    allow_headers = ["*"]
)

@app.get('/')
def main():
    return {"message": "hello world"}