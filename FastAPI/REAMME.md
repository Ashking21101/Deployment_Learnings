uvicorn app:app --reload



# fastapi
path params = @app.get("/patients/{record_id}"). -> required in CRUD
status code = HttpExecption
Query params(sorting/ordering/filtering) = http://127.0.0.1:8000/sort?sort_by=diagnosis&order_by=desc


# pydantic
optional        = optional fields
EmailStr        = for Emial datatype (data validation)
anyurl          = for website or any other url (data validation)
field           =  for default_value, max_length, min_length (data validation)
Annotated       = for metadata/description,
field_validator = custom data validation for single field (email = 'hdfc.com'etc), data transformation
model_validator = custom data validation for our entire model fields alltogether
computed fields = for our own calculated field
nested model    = for model inside a model (like address) 
serialization   = temp = patient1.model_dump() , this is to export model Objects, in json/dict
 






##status codes
______________________________________________
| Series  | Meaning      | In Simple Words   |
| ------- | ------------ | ----------------- |
|   2xx   | Success      | Request worked    |
|   3xx   | Redirection  | Go somewhere else |
|   4xx   | Client Error | Your mistake      |
|   5xx   | Server Error | Server’s mistake  |
______________________________________________



_______________________________________________________________________________________________________
| Code    | Name                   | Meaning                            | Typical Use Case            |
| ------- | ---------------------- | ---------------------------------- | --------------------------- |
|   200   | OK                     | Request succeeded                  | Successful GET / PUT        |
|   403   | Forbidden              | Access denied                      | No permission               |
|   404   | Not Found              | Resource not found                 | Invalid endpoint / ID       |
_______________________________________________________________________________________________________

