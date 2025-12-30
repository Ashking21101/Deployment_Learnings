from fastapi import FastAPI,Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json 


app = FastAPI()


class Patient(BaseModel):
    record_id: Annotated[str, Field(..., example="R001", description="Unique identifier for the patient record")]
    patient_name: Annotated[str, Field(..., example="Rahul Mehta", description="Full name of the patient")]
    city: Annotated[str, Field(..., example="Mumbai", description="City where the patient resides")]
    age: Annotated[int, Field(..., ge=0, le=120, example=28, description="Age of the patient in years")]
    gender: Annotated[Literal["Male", "Female", "Other"], Field(..., example="Male", description="Gender of the patient")]
    height_cm: Annotated[float, Field(..., ge=50, le=250, example=172, description="Height of the patient in centimeters")]
    weight_kg: Annotated[float, Field(..., ge=2, le=300, example=68, description="Weight of the patient in kilograms")]


    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight_kg / ((self.height_cm / 100) ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"



# we are creating an seperate UPDATE model/schema coz we cant use the same model for both CREATE and UPDATE operations
class Patient_update(BaseModel):
    patient_name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, ge=0)]
    gender: Annotated[Optional[Literal["Male", "Female", "Other"]], Field(default=None)]
    height_cm: Annotated[Optional[float], Field(default=None)]
    weight_kg: Annotated[Optional[float], Field(default=None)] 








def load_data():
    with open("/Users/ashishtak/FastAPI_Tutorial/data.json", "r") as file:
        data = json.load(file)
    return data

def save_data(data):
    with open("/Users/ashishtak/FastAPI_Tutorial/data.json", "w") as file:
        json.dump(data, file, indent=4)


@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"app": "FastAPI Tutorial", "version": "1.0.0"}

@app.get("/view")
def view():
    data = load_data()
    return data


# so what we did is add Path Parameter  
# Path "..." says that it is a required parameter
# path description is added for info purpose
@app.get("/patients/{record_id}")#actual Path Params in the URL
def get_patient(record_id: str = Path(..., description="The ID of the patient record to retrieve"), example="R001"):
    data = load_data()
    if record_id in data:
        return data[record_id]
    raise HTTPException(status_code = 404, detail = "Patient not found")
#   return {"error": "Patient not found"} --> when not found it says status is 200 i.e. successfull but we want to show 404 error




# Query Parameters
# ... means required parameter
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort by field like record_id, doctor_name"),
                  order_by: str = Query("asc", description="Order by asc or desc")):
     
    valid = ["record_id", "doctor_name", "patient_name", "diagnosis"]

    if sort_by not in valid:
        raise HTTPException(status_code=400, detail="Invalid sort_by parameter")
    if order_by not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order_by parameter")


    data = load_data()
    sort_order = True if order_by == "asc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=sort_order)
    return sorted_data


@app.post("/create")
def create_patient(patient : Patient):
    # load data-> check if the new record is there in old data -> if not add it -> save it
    data = load_data() 
    # 'data' is a python dictionary
    # 'patient' is pydantic model object
    if patient.record_id in data:
        raise HTTPException(status_code=400, detail = "Record ID already exists")

    # convert pydantic model to dictionary using model_dump
    data[patient.record_id] = patient.model_dump() # exclude = ["record_id"]

    # convert back to json and save
    save_data(data)
    # well the create operation can be does via SWAGGER UI only , ib this case
    return JSONResponse(status_code= 201, content = {"message": "Patient record created successfully"})


@app.put("/edit/{record_id}")
def update_patient(record_id: str, patient_update: Patient_update):
    data = load_data()

    if record_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    existing_patient_info = data[record_id]

    # convert patient_update from pydantic model to dictionary using model_dump
    update_patient_info = patient_update.model_dump(exclude_unset = True) 
    # exclude_unset ensures that only the fields that are provided in the update request are included in the resulting dictionary
    # since we have added 'none' as default value for all fields in update model and we dont want null vales

    for key, value in update_patient_info.items():
        existing_patient_info[key] = value
    

    # one issue is that if we update height or weight , bmi and verdict will not be updated
    # so we will convert existing_patient_info to Patient model and then back to dictionary
    # so that computed fields are recalculated

    patient_pydantic_obj = Patient(**existing_patient_info) # unpacking dictionary to pydantic model along with computed fields
    existing_patient_info = patient_pydantic_obj.model_dump()  #converting back to dictionary

    data[record_id] = existing_patient_info
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient record updated successfully"})


@app.delete("/delete/{record_id}")
def delete_patient(record_id: str):
    data = load_data()

    if record_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[record_id]
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient record deleted successfully"})
