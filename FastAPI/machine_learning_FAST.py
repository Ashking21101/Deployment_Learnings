from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing_extensions import Annotated, Literal
import joblib
import pandas as pd
from fastapi.responses import JSONResponse   

# =========================
# 1. LOAD MODEL & ENCODERS
# =========================
model = joblib.load("model.pkl")
encoders = joblib.load("encoders.pkl")
target_encoder = joblib.load("target_encoder.pkl")

app = FastAPI(title="Insurance Premium Prediction API")

# =========================
# 2. INPUT SCHEMA
# =========================
class InsuranceInput(BaseModel):
    age: Annotated[int,Field(...,gt=0,lt=120,description="Age of the user",example=35)]
    weight: Annotated[float,Field(...,gt=0,description="Weight of the user in kg",example=78.5)]
    height: Annotated[float,Field(...,gt=0,lt=2.5,description="Height of the user in meters",example=1.72)]
    income_lpa: Annotated[float,Field(...,gt=0,description="Annual income of the user in LPA",example=12.5)]
    smoker: Annotated[bool,Field(...,description="Is the user a smoker?",example=False)]
    city: Annotated[Literal["Mumbai", "Delhi", "Bangalore", "Pune", "Lucknow"],Field(...,description="City where the user lives",example="Pune")]
    occupation: Annotated[Literal["retired","freelancer","student","government_job","business_owner","unemployed","private_job"],
        Field(...,description="Occupation of the user",example="private_job")]

# =========================
# =========================

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 30:
            return "young"
        elif self.age < 55:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        return "low"

    @computed_field
    @property
    def city_tier(self) -> int:
        city_tier_map = {
            "Mumbai": 1,
            "Delhi": 1,
            "Bangalore": 1,
            "Pune": 2,
            "Lucknow": 2
        }
        return city_tier_map.get(self.city, 3)
    

    ### =========================
    ### 3. PREDICTION ENDPOINT
    ### =========================
@app.post("/predict")
def predict_premium(data: InsuranceInput):

    input_df = pd.DataFrame([{
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



















    # Encode only required columns
    for col in input_df.columns:
        if col in encoders:
            input_df[col] = encoders[col].transform(input_df[col])

    prediction = model.predict(input_df)[0]
    result = target_encoder.inverse_transform([prediction])[0]

    return {"insurance_premium_category": result}
