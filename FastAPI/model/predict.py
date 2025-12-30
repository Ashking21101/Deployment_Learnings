import joblib
import pandas as pd
from fastapi.responses import JSONResponse   
import os


# =========================
# PATH SETUP (Docker-safe)
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")

model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
encoders = joblib.load(os.path.join(MODEL_DIR, "encoders.pkl"))
target_encoder = joblib.load(os.path.join(MODEL_DIR, "target_encoder.pkl"))




# =========================
# 1. LOAD MODEL & ENCODERS
# =========================
#model = joblib.load("/Users/ashishtak/FastAPI_Tutorial/Fast_project/model/model.pkl")
#encoders = joblib.load("/Users/ashishtak/FastAPI_Tutorial/Fast_project/model/encoders.pkl")
#target_encoder = joblib.load("/Users/ashishtak/FastAPI_Tutorial/Fast_project/model/target_encoder.pkl")

MODEL_VERSION = "1.0.0"


##########################
def predict_output(input_df: pd.DataFrame) -> str:
    """
    Takes a pandas DataFrame and returns decoded prediction
    """

    for col in input_df.columns:
        if col in encoders:
            input_df[col] = encoders[col].transform(input_df[col])

    prediction = model.predict(input_df)[0]
    result = target_encoder.inverse_transform([prediction])[0]

    return result    
