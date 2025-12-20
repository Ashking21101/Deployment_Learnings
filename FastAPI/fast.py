from fastapi import FastAPI,Path, HTTPException, Query
from pydantic import BaseModel
import json 


app = FastAPI()

def load_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return data


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