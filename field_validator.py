from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

# field validator here we are making a custom data validation
class Patient(BaseModel):

    name : str
    age : int
    email : EmailStr
    url : AnyUrl
    weight : float
    height : float
    married : bool
    allergies : Optional[List[str]] = None # optional if not having the data....List[str] to go though the data inside the list
    contact_details : Dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validation(cls, value):
        valid_domain = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domain:
            raise ValueError('Not a valid domain')
    
        return value
    
    #if we want any transformation 
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    #if we want to make custom validator with diff. field toghetr
    @model_validator(mode='after')
    def validator_emergency(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patient need to have emergency no.')
        return model
    
    #if esnt to calc new data taking the pateint feild
    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi


def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.calculate_bmi)
    print('inserted')


    

patient_info = {'name':'bednata', 'age': 40, 'email' : 'abc@hdfc.com', 'url' : 'https://www.linkedin.com/feed/', 'weight':40.6, 'height':1.78, 'married':True, 'allergies':['dust', 'viral'], 'contact_details':{'phone no':'28629234', 'emergency':"96378429"}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)