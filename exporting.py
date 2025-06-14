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

temp = patient1.model_dump()
# temp = patient1.model_dump(include=['name', 'gender']), exclude=[], exclude_unset=True we write it so that the field not given in dict are not allowed

print(temp)
print(type(temp))

