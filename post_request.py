from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()


def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)





@app.get("/")
def hello():
    return {'message':'Patients Management System API'}

    
@app.get("/about")
def about():
    return {'message':'A fully functional API to manage your patients records'}

@app.get('/view')
def view():
    data = load_data()
    return data

#path -- they are the type of parameters which are dynamic part of the url through which we can fetch particular data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(...,description='Id of the patient', example='P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='patient not found')     #showing the right status code 





class Patient(BaseModel):
    
    id: Annotated[str, Field(..., description="id of the patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="Name of the Patient")]
    city: Annotated[str, Field(..., description="name of the city")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="age of the patient")]
    gender: Annotated[Literal['male','female','others'], Field(..., description="gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="height of the patient in mtrs")]
    weight: Annotated[float, Field(..., gt=0, description="weight of the patient kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'under weight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obicity'
        

@app.post('/create')
def create_patient(patient : Patient):

    #load existing data
    data = load_data()

    #check if the pateint is already there
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient is already there')
    

    #new pateint add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    #save into 
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created sucessfully'})

