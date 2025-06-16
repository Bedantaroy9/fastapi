from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
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




@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight, bmi'), order : str=Query('asc', description='order in asc pr desc')):

    valid_field = ['height', 'weight', 'bmi']

    if sort_by not in valid_field:
        raise HTTPException(status_code=400, detail=f'Invalid feild select from {valid_field}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail='Invaloid order not found') #if no order is set the default is asc
    
    data = load_data()

    sorted_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sorted_order) #sort?sort_by=height&order=desc

    return sorted_data



#creating 
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


#for updating

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male','female','others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate): #Take the request body...Parse the JSON into a PatientUpdate object
                                 
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='pattient not exist')
    
    existing_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True) #it maily taking the changes made by the user.... converts the patient_update Pydantic model into a dictionary 
    #r because PatientUpdate is a class, not an instance.

    for key, value in updated_patient_info.items():
        existing_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_info)
    #-> pydantic object -> dict
    existing_info = patient_pydantic_obj.model_dump(exclude='id')

    #add this dict data
    data[patient_id] = existing_info

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='patient not exist')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'}) 

    