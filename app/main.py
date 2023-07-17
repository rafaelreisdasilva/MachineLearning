#!pip install fastapi
#!pip install uvicorn
from fastapi import FastAPI
import logging
from pydantic import BaseModel #
from app.model import predict

#creating the logs
logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w", format="%(asctimea)s - %(levelname)s - %(message)s")


#creating the app
app = FastAPI()

#home route
@app.get("/")
def home():
    #try:
    return "<table></table>"
    #except ZeroDivisionError as e:
        #logging.error("ZeroDivisionError",exc_info=True)
        #logging.exception("Error")