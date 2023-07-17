#!pip install fastapi
#!pip install uvicorn
from fastapi import FastAPI
import logging

#creating the logs
logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w", format="%(asctimea)s - %(levelname)s - %(message)s")


#creating the app
app = FastAPI()


@app.get("/")
def index():
    #try:
    return {"title":"ola"}
    #except ZeroDivisionError as e:
        #logging.error("ZeroDivisionError",exc_info=True)
        #logging.exception("Error")