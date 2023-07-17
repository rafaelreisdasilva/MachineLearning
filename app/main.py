#!pip install fastapi
#!pip install uvicorn

import logging
import pandas
import json
from fastapi import FastAPI
from pydantic import BaseModel #data validation
from .model.modelApiEndpoint import getPredictionFromTestByIndex
from .model.modelApiEndpoint import __version__ as model_version
from pathlib import Path
from fastapi.responses import HTMLResponse

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
@app.get("/predictFromTestByIndex")
def predictionFromTestByIndex():
    return getPredictionFromTestByIndex()
    #return HTMLResponse(content=getPredictionFromTestByIndex(id_line), status_code=200)