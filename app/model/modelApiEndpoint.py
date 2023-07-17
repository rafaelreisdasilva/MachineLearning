
import pickle
import logging
import pandas as pd
from pathlib import Path
test_path= "test.csv"

__version__ = "0.1.0" #current version of my model

#creating the logs
logging.basicConfig(level=logging.INFO, filename="log_modelApiEndPoint.log", filemode="w", format="%(asctimea)s - %(levelname)s - %(message)s")

Base_DIR = Path(__file__).resolve(strict=True).parent


with open(f"{Base_DIR}/trained_pipeline-{__version__}.pkl","rb") as f:
    model = pickle.load(f) #load the model


def predict_pipepline_from_path(path):
    df_file=''
    try:
        df_file = pd.read_csv(path, index_col=False)
    except FileNotFoundError:
        logging.warning('File not found.')
    
    model.predict(df_file)

def getPredictionFromTestByIndex(index):
    test = pd.read_csv(test_path)
    return model.predict(test.loc[[index]])
