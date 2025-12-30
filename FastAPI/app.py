from unittest import result
from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing_extensions import Annotated, Literal
import joblib
import pandas as pd
from fastapi.responses import JSONResponse   
from schema.user_input import InsuranceInput
from model.predict import predict_output, MODEL_VERSION
from schema.prediction_response_model import PredictionResponse


app = FastAPI(title="Insurance Premium Prediction API")

# =========== pydantic MODEL ==============
# schema/user_input.py Pydantic MODEL needs to be imported here


@app.get("/")
def home():
    return {"message": "Insurance Premium Prediction API"}


@app.get("/health")# required for AWS deployment, they will force us to make this endpoint
def health():
    return {"status": "ok", 'version': MODEL_VERSION, 'model_loaded': True}



@app.post("/predict")
def predict_premium(data: InsuranceInput):

    user_input = pd.DataFrame([{
    # RAW FEATURES
    "age": data.age,
    "weight": data.weight,
    "height": data.height,
    "income_lpa": data.income_lpa,
    "smoker": data.smoker,
    "city": data.city,
    "occupation": data.occupation,

    # ENGINEERED FEATURES
    "bmi": data.bmi,
    "age_group": data.age_group,
    "lifestyle_risk": data.lifestyle_risk,
    "city_tier": data.city_tier
    }])

    try:
        predict = predict_output(user_input)
        return JSONResponse(content={"insurance_premium_category": predict})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)




@app.post("/predict", response_model=PredictionResponse)
def predict_premium(data: InsuranceInput):

    input_df = pd.DataFrame([{
        "age": data.age,
        "weight": data.weight,
        "height": data.height,
        "income_lpa": data.income_lpa,
        "smoker": data.smoker,
        "city": data.city,
        "occupation": data.occupation,
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier
    }])

    prediction = predict_output(input_df)

    return JSONResponse(
        content={"insurance_premium_category": prediction}
    )
