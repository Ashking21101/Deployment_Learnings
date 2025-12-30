from pydantic import BaseModel, Field, computed_field
from typing import Dict

class PredictionResponse(BaseModel):
    predicted_category: str = Field(..., description="Predicted insurance premium category", example="medium")