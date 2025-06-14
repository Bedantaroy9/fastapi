from pydantic import BaseModel

class Address(BaseModel):
    city : str
    state : str
    pin : str

class Patient(BaseModel):
    name : str
    gender : str
    age : int
    address : Address

address_dict = {'city':'delhi', 'state':'assam', 'pin':'267892'}

address1 = Address(**address_dict) 

patient_dict = {'name':'bedanta', 'gender':'male', 'age':85, 'address':address1}

patient1 = Patient(**patient_dict)

print(patient1.name)
print(patient1.address.pin)