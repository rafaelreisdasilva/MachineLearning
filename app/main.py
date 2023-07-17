#!pip install fastapi
#!pip install uvicorn
from fastapi import FastAPI
from pydantic import BaseModel #data validation
import logging
from app.model.modelApiEndpoint import getPredictionFromTestByIndex
from app.model.modelApiEndpoint import __version__ as model_version
from pathlib import Path

Base_TEST_DIR = "./model/test.csv"

#creating the app
app = FastAPI()


 
#creating the logs
logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w", format="%(asctimea)s - %(levelname)s - %(message)s")

#home route
@app.get("/")
def home():
    #try:
    return "<table></table>"
    #except ZeroDivisionError as e:
        #logging.error("ZeroDivisionError",exc_info=True)
        #logging.exception("Error")


#class PredictionPath(BaseModel)
@app.get("/predictFromTestByIndex/{id_line}")
def predictionFromTestByIndex(id_line=int):
    return getPredictionFromTestByIndex(id_line)