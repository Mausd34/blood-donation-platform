from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Literal

app=FastAPI(title='Blood Donation Platform API',version='2.0.0')
donors=[]; requests=[]
BloodGroup=Literal['A+','A-','B+','B-','AB+','AB-','O+','O-']
class Donor(BaseModel): name:str=Field(min_length=2); blood_group:BloodGroup; city:str; phone:str; available:bool=True
class BloodRequest(BaseModel): patient:str=Field(min_length=2); blood_group:BloodGroup; city:str; units:int=Field(gt=0,le=20); urgent:bool=False
@app.get('/health')
def health(): return {'status':'ok','service':'blood-donation-platform','version':'2.0.0'}
@app.post('/donors')
def add_donor(d:Donor):
    item={'id':len(donors)+1,**d.model_dump()}; donors.append(item); return item
@app.get('/donors')
def find_donors(blood_group:BloodGroup|None=None,city:str|None=None):
    return [d for d in donors if d['available'] and (not blood_group or d['blood_group']==blood_group) and (not city or d['city'].lower()==city.lower())]
@app.post('/requests')
def create_request(r:BloodRequest):
    item={'id':len(requests)+1,**r.model_dump(),'status':'open'}; requests.append(item); return item
@app.get('/requests')
def list_requests(): return requests
@app.get('/dashboard')
def dashboard(): return {'donors':len(donors),'available_donors':sum(d['available'] for d in donors),'open_requests':sum(r['status']=='open' for r in requests),'urgent_requests':sum(r['urgent'] for r in requests if r['status']=='open')}
app.mount('/',StaticFiles(directory='web',html=True),name='web')
