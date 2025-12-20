from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated 


# nested model example
class address1(BaseModel):
    street : str
    city : str
    state : str
    zip_code : str



class Patient(BaseModel): # bydefault all required fields
    name : Annotated[str ,Field(default=None, max_length=50, min_length=2, description="Full name of the patient", title="Patient Name")]
    age : int = Field(gt=0, lt=120) # > and <
    weight : Annotated[float , Field(gt=0, strict=True)] # > 0, strict=True means no internal conversion "2.5" to 2.5 not done automatically
    married : bool
    allergies : list[str] # why not just list and why list[str] coz we need to validate its a list and its elements are str
    contacts : Optional[Dict[str, str]]=None # key=str, value=str
    email : EmailStr
    website : AnyUrl
    address : address1 # for nested model



    # for our custom validation applying on the field email
    @field_validator('email') 
    @classmethod
    def custom_email(cls,value): # cls is the class itself and value is the value of the field email
        valid_domain = ['hdfc.com', 'icici.com']
        domain = value.split('@')[-1]
        if domain not in valid_domain:
            raise ValueError(f"Email domain must be one of {valid_domain}")
        return value


    # for our custom transformation applying on the field 'name'
    @field_validator('name') 
    @classmethod
    def transform_name(cls,value):
        return value.upper()



    # model level validation (no need to specify field name coz it applies to the whole model)
    @model_validator(mode = 'after')
    def validate_ememgency_contact(self):
        if self.age > 60 and 'emergency' not in self.contacts:
            raise ValueError("emergency contact is required for patients below 60 years of age")
        else:
            return self


    # calculated field
    @computed_field
    @property
    def bmi(self) -> float: # return type float
        bmi = round(self.weight/(self.age**2) , 2)
        return bmi




def insert_patient(patient : Patient):
    print(f"Inserting patient: {patient.name}, Age: {patient.age}, Weight: {patient.weight}, Married: {patient.married}, Allergies: {patient.allergies}, Contacts: {patient.contacts}, Email: {patient.email}, Website: {patient.website}, BMI: {patient.bmi}, Address: {patient.address}")

def update_patient(patient: Patient):
    print(f"Updating patient to Name: {patient.name}, Age: {patient.bmi}")


# we need address model to pass in patient model
address_dict = {'street':'123 Main St', 'city':'Metropolis', 'state':'NY', 'zip_code':'10001'}
address = address1(**address_dict)


patient1 = {'name':'John Doe', 'age':'30',  # see age is str but as our basemodel age is int so pydantic will convert it automatically
            'weight':70.5, 'married':True, 
            'allergies':['pollen', 'nuts'], 
            'contacts':{'primary':'8850644571'},
            'email':'john.doe@hdfc.com',
            'website':'https://www.johndoe.com',
            'address': address
            }
insert_patient(Patient(**patient1))



# serialization
#temp = patient.model_dump() # returns a dict
#print(temp)
#print(type(temp))