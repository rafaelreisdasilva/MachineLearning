#!pip install fastapi
#!pip install uvicorn

import logging
import pandas
import json
from fastapi import FastAPI,Request
from pydantic import BaseModel #data validation
from .model.modelApiEndpoint import getPredictionFromTestByIndex
from .model.modelApiEndpoint import __version__ as model_version
from pathlib import Path
from fastapi.responses import HTMLResponse
from fastapi import HTTPException, status, Security, FastAPI
from fastapi.security import APIKeyHeader, APIKeyQuery
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


API_KEYS = [
    "9d207bf0-10f5-4d8f-a479-22ff5aeff8d1",
    "f47d4a2c-24cf-4745-937e-620a5963c0b8",
    "b7061546-75e8-444b-a2c4-f19655d07eb8",
]

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
) -> str:
    """Retrieve and validate an API key from the query parameters or HTTP header.

    Args:
        api_key_query: The API key passed as a query parameter.
        api_key_header: The API key passed in the HTTP header.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If the API key is invalid or missing.
    """
    if api_key_query in API_KEYS:
        return api_key_query
    if api_key_header in API_KEYS:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )




#creating the app
app = FastAPI()


 
#creating the logs
logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w", format="%(asctimea)s - %(levelname)s - %(message)s")

#home route
@app.get("/")
def home():
    html_content = """
    <html>
        <head>
            <title>Estimating property valuations</title>
            <style>
                 th, td {
                    border-color: #96D4D4;
                 }
            </style>
        </head>
        <body>
            <p>Hi</p>
          
            <p>To enhance the model's accuracy, categorical variables were included in the learning process. As a result, the file includes the following fields:</p>

            <ul>
                <li>net_usable_area</li>
                <li>net_area</li>
                <li>n_rooms</li>
                <li>n_bathroom</li>
                <li>latitude</li>
                <li>longitude</li>
                <li>price</li>
                <li>la reina</li>
                <li>las condes</li>
                <li>lo barnechea</li>
                <li>nunoa</li>
                <li>providence</li>
                <li>vitacura</li>
                <li>house</li>
                <li>department</li>
                <li>bathroom_ratio</li>
                <li>household_rooms</li>
            </ul>

            <p>To handle the initial categories, #n-1 dummy variables were utilized, effectively avoiding arbitrary weighting errors.</p>
            <br>
            <table style="width:100%">
               <tr><td><b>URL</b></td><td><b>Description</b></td><td><b>How to use</b></td><td><b>Restrictions</b></td></tr>
                
                <tr><td><b>/predictionsPassingTheCsvFilename/filename</b></td><td>The purpose of this method is to return the estimated price from a csv file</td>
                <td>You must upload the file in the learningFiles folder and pass the file name as a parameter, without the format.</td></tr>


            </table>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
    #try:
    #except ZeroDivisionError as e:
        #logging.error("ZeroDivisionError",exc_info=True)
        #logging.exception("Error")

@app.get("/predictionsPassingTheCsvFilename/{name}")
def predictionsByCsv(name=str):
    """A function that returns price predictions to a csv file stored in the learningFiles folder."""
    try:
        return getPredictionFromTestByIndex(name)
    except ValueError as e:
        logging.error("ValueError",exc_info=True)
        logging.exception("Error")


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
  return JSONResponse(status_code=500, content=jsonable_encoder({"code": 500, "msg": "Unexpected value"}))





#To test the API key authentication, you can use tools like cURL or Postman.
@app.get("/private")
def private(api_key: str = Security(get_api_key)):
    """A private endpoint that requires a valid API key to be provided."""
    return f"Private Endpoint. API Key: {api_key}" 