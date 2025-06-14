from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

#BaseModel is used to create data models with built-in validation and parsing.
class Patient(BaseModel):

    name : Annotated[str, Field(max_length=50, title='Name of the person', description='give name in 50 chars', examples=['bedanta', 'alvish'])] # applied field and also given meta data to it 
    age : int
    email : EmailStr
    url : AnyUrl
    weight : float = Field(gt=0, lt=120, strict=True) #value should be greater than 0, strict for only float not str
    married : Annotated[bool, Field(default=None)]
    allergies : Optional[List[str]] = None # optional if not having the data....List[str] to go though the data inside the list
    contact_details : Dict[str, str]



def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print('inserted')


patient_info = {'name':'bednata', 'age': 40, 'email' : 'abc@gmail.com', 'url' : 'https://www.linkedin.com/feed/', 'weight':40.6, 'married':True, 'allergies':['dust', 'viral'], 'contact_details':{'email':'abc@gmail.com','phone no':'28629234'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)

