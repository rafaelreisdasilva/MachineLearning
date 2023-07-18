#!pip install fastapi
#!pip install uvicorn

import logging
import pandas as pd
from fastapi import FastAPI,Request,  Form
from pydantic import BaseModel #data validation
from .model.modelApiEndpoint import getPredictionFromTestByIndex, getPredictionFromForm
from .model.modelApiEndpoint import __version__ as model_version
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


# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

#creating the logs
logging.basicConfig(level=logging.DEBUG, filename="log_general.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")

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
        <input type="checkbox" name="la_reina" id="la_reina"  value="true"><br>

        <label for="las_condes">las condes:</label>
        <input type="checkbox" name="las_condes" id="las_condes"  value="true"><br>

        <label for="lo_barnechea">lo barnechea:</label>
        <input type="checkbox" name="lo_barnechea" id="lo_barnechea"  value="true"><br>

        <label for="nunoa">nunoa:</label>
        <input type="checkbox" name="nunoa" id="nunoa"  value="true"><br>

        <label for="providence">providence:</label>
        <input type="checkbox" name="providence" id="providence"  value="true"><br>

        <label for="vitacura">vitacura:</label>
        <input type="checkbox" name="vitacura" id="vitacura"  value="true"><br>

        <label for="house">house:</label>
        <input type="checkbox" name="house" id="house"  value="true"><br>

        <label for="department">department:</label>
        <input type="checkbox" name="department" id="department"  value="true"><br>

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


@app.post("/")
async def process_form(
    net_usable_area: int = Form(...),
    net_area: int = Form(...),
    n_rooms: int = Form(...),
    n_bathroom: int = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    price: int = Form(...),
    la_reina: bool = Form(...),
    las_condes: bool = Form(...),
    lo_barnechea: bool = Form(...),
    nunoa: bool = Form(...),
    providence: bool = Form(...),
    vitacura: bool = Form(...),
    house: bool = Form(...),
    department: bool = Form(...),
    bathroom_ratio: int = Form(...),
    household_rooms: int = Form(...)
):
    try:
        data = {
            "net_usable_area": net_usable_area,
            "net_area": net_area,
            "n_rooms": n_rooms,
            "n_bathroom": n_bathroom,
            "latitude": latitude,
            "longitude": longitude,
            "price": price,
            "la_reina": la_reina,
            "las_condes": las_condes,
            "lo_barnechea": lo_barnechea,
            "nunoa": nunoa,
            "providencia": providence,
            "vitacura": vitacura,
            "casa": house,
            "departamento": department,
            "bathroom_ratio": bathroom_ratio,
            "household_rooms": household_rooms
        }
        df = pd.DataFrame([data])
        prediction = getPredictionFromForm(df)
        return prediction.tolist()
    except Exception as e:
        return {"error": str(e)}

'''
# URL do seu servidor FastAPI
url = "http://localhost:80"

# Parâmetros do formulário
params = {
    "net_usable_area": 100,
    "net_area": 120,
    "n_rooms": 3,
    "n_bathroom": 2,
    "latitude": 123.456,
    "longitude": -45.678,
    "price": 200000,
    "la_reina": True,
    "las_condes": False,
    "lo_barnechea": True,
    "nunoa": False,
    "providence": True,
    "vitacura": False,
    "house": True,
    "department": False,
    "bathroom_ratio": 2,
    "household_rooms": 4
}

# Enviar a requisição POST
response = requests.post(url, data=params)

# Verificar a resposta
if response.status_code == 200:
    print("Formulário enviado com sucesso!")
else:
    print("Ocorreu um erro ao enviar o formulário.")

'''