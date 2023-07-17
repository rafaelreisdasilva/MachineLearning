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
from imp import reload 

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
logging.basicConfig(level=logging.DEBUG, filename="log_general.log", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")

#home route
@app.get("/")
def home():
    logging.info("main page access")
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
                <li>net_usable_area (int)</li>
                <li>net_area (int) </li>
                <li>n_rooms (int)</li>
                <li>n_bathroom (int)</li>
                <li>latitude (float)</li>
                <li>longitude(float)</li>
                <li>price (int)</li>
                <li>la reina(bool)</li>
                <li>las condes(bool)</li>
                <li>lo barnechea(bool)</li>
                <li>nunoa(bool)</li>
                <li>providence(bool)</li>
                <li>vitacura(bool)</li>
                <li>house(bool)</li>
                <li>department(int)</li>
                <li>bathroom_ratio(int)</li>
                <li>household_rooms(int)</li>
            </ul>

            <p>To handle the initial categories, #n-1 dummy variables were utilized, effectively avoiding arbitrary weighting errors.</p>
            <br>
           <table style="width:100%">
            <tr>
                <th>URL</th>
                <th>Description</th>
                <th>How to Use</th>
                <th>Restrictions</th>
            </tr>
            <tr>
                <td><code>/predictionsPassingTheCsvFilename/filename</code></td>
                <td>This method retrieves the estimated price from a CSV file.</td>
                <td>To use this method, you need to upload the file to the "learningFiles" folder and pass the file name as a parameter without the file format extension.</td>
                <td>None</td>
            </tr>
            </table>

        <br>
        <form action="/" method="post">
        <label for="net_usable_area">net_usable_area:</label>
        <input type="number" name="net_usable_area" id="net_usable_area" required><br>

        <label for="net_area">net_area:</label>
        <input type="number" name="net_area" id="net_area" required><br>

        <label for="n_rooms">n_rooms:</label>
        <input type="number" name="n_rooms" id="n_rooms" required><br>

        <label for="n_bathroom">n_bathroom:</label>
        <input type="number" name="n_bathroom" id="n_bathroom" required><br>

        <label for="latitude">latitude:</label>
        <input type="number" step="any" name="latitude" id="latitude" required><br>

        <label for="longitude">longitude:</label>
        <input type="number" step="any" name="longitude" id="longitude" required><br>

        <label for="price">price:</label>
        <input type="number" name="price" id="price" required><br>

        <label for="la_reina">la reina:</label>
        <input type="checkbox" name="la_reina" id="la_reina"><br>

        <label for="las_condes">las condes:</label>
        <input type="checkbox" name="las_condes" id="las_condes"><br>

        <label for="lo_barnechea">lo barnechea:</label>
        <input type="checkbox" name="lo_barnechea" id="lo_barnechea"><br>

        <label for="nunoa">nunoa:</label>
        <input type="checkbox" name="nunoa" id="nunoa"><br>

        <label for="providence">providence:</label>
        <input type="checkbox" name="providence" id="providence"><br>

        <label for="vitacura">vitacura:</label>
        <input type="checkbox" name="vitacura" id="vitacura"><br>

        <label for="house">house:</label>
        <input type="checkbox" name="house" id="house"><br>

        <label for="department">department:</label>
        <input type="checkbox" name="department" id="department"><br>

        <label for="bathroom_ratio">bathroom_ratio:</label>
        <input type="number" name="bathroom_ratio" id="bathroom_ratio" required><br>

        <label for="household_rooms">household_rooms:</label>
        <input type="number" name="household_rooms" id="household_rooms" required><br>

        <input type="submit" value="Enviar">
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
    logging.info("user wanted to predict data from file "+name+".csv")
    """A function that returns price predictions to a csv file stored in the learningFiles folder."""
    """Please note that the .csv at the end of the file name is not required """
    try:
        return getPredictionFromTestByIndex(name)
    except ValueError as e:
        logging.error("ValueError",exc_info=True)
        logging.exception("Error")


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
  logging.info("Error 500")
  return JSONResponse(status_code=500, content=jsonable_encoder({"code": 500, "msg": "Unexpected value"}))

@app.exception_handler(400)
async def internal_exception_handler(request: Request, exc: Exception):
  logging.info("Error 400")
  return JSONResponse(status_code=400, content=jsonable_encoder({"code": 400, "msg": "Unexpected value"}))

@app.exception_handler(422)
async def internal_exception_handler(request: Request, exc: Exception):
  logging.info("Error 422")
  return JSONResponse(status_code=422, content=jsonable_encoder({"code": 422, "msg": "Validation Error"}))

#To test the API key authentication, you can use tools like cURL or Postman.
@app.get("/private")
def private(api_key: str = Security(get_api_key)):
    logging.info("Access to a private endpoint")
    """A private endpoint that requires a valid API key to be provided."""
    return f"Private Endpoint. API Key: {api_key}" 