#!pip install fastapi
#!pip install uvicorn
from fastapi import FastAPI

app = FastApi()

@app.get(/)
def index():
    return {"title":"ola"}