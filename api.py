from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal

app=FastAPI(title='Blood Donation Platform API',version='1.0.0')
donors=[]; requests=[]
class Donor(BaseModel): name:str; blood_group:Literal['A+','A-','B+','B-','AB+','AB-','O+','O-']; city:str; phone:str; available:bool=True
class BloodRequest(BaseModel): patient:str; blood_group:Literal['A+','A-','B+','B-','AB+','AB-','O+','O-']; city:str; units:int=Field(gt=0,le=20); urgent:bool=False
@app.get('/health')
def health(): return {'status':'ok','service':'blood-donation-platform'}
@app.post('/donors')
def add_donor(d:Donor):
    item={'id':len(donors)+1,**d.model_dump()}; donors.append(item); return item
@app.get('/donors')
def find_donors(blood_group:str|None=None,city:str|None=None):
    return [d for d in donors if d['available'] and (not blood_group or d['blood_group']==blood_group) and (not city or d['city'].lower()==city.lower())]
@app.post('/requests')
def create_request(r:BloodRequest):
    item={'id':len(requests)+1,**r.model_dump(),'status':'open'}; requests.append(item); return item
@app.get('/requests')
def list_requests(): return requests
