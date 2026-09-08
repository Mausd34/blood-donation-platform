from fastapi import FastAPI,HTTPException,Depends
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel,Field
from typing import Literal
from app.auth import hash_password,create_token,verify_token
from app.db import connect,init_db
app=FastAPI(title='Blood Donation Platform API',version='4.0.0');init_db();security=HTTPBearer(auto_error=False)
donors=[];requests=[];BloodGroup=Literal['A+','A-','B+','B-','AB+','AB-','O+','O-']
class Credentials(BaseModel):username:str=Field(min_length=3,max_length=80);password:str=Field(min_length=6,max_length=200)
class Donor(BaseModel):name:str=Field(min_length=2);blood_group:BloodGroup;city:str;phone:str;available:bool=True
class BloodRequest(BaseModel):patient:str=Field(min_length=2);blood_group:BloodGroup;city:str;units:int=Field(gt=0,le=20);urgent:bool=False
def current_user(c:HTTPAuthorizationCredentials=Depends(security)):
    if not c:raise HTTPException(401,'Authentication required')
    u=verify_token(c.credentials)
    if not u:raise HTTPException(401,'Invalid or expired token')
    return u
@app.get('/health')
def health():return {'status':'ok','service':'blood-donation-platform','version':'4.0.0'}
@app.post('/auth/register')
def register(b:Credentials):
    with connect() as c:
        if c.execute('SELECT 1 FROM users WHERE username=?',(b.username,)).fetchone():raise HTTPException(409,'Username already exists')
        c.execute('INSERT INTO users(username,password_hash) VALUES(?,?)',(b.username,hash_password(b.password)));c.commit()
    return {'message':'registered','username':b.username}
@app.post('/auth/login')
def login(b:Credentials):
    with connect() as c:u=c.execute('SELECT * FROM users WHERE username=?',(b.username,)).fetchone()
    if not u or u['password_hash']!=hash_password(b.password):raise HTTPException(401,'Invalid username or password')
    return {'access_token':create_token(u['username']),'token_type':'bearer'}
@app.get('/auth/me')
def me(u=Depends(current_user)):return u
@app.post('/donors')
def add_donor(d:Donor,u=Depends(current_user)):
    item={'id':len(donors)+1,**d.model_dump()};donors.append(item);return item
@app.get('/donors')
def find_donors(blood_group:BloodGroup|None=None,city:str|None=None,u=Depends(current_user)):
    return [d for d in donors if d['available'] and (not blood_group or d['blood_group']==blood_group) and (not city or d['city'].lower()==city.lower())]
@app.post('/requests')
def create_request(r:BloodRequest,u=Depends(current_user)):
    item={'id':len(requests)+1,**r.model_dump(),'status':'open'};requests.append(item);return item
@app.get('/requests')
def list_requests(u=Depends(current_user)):return requests
@app.get('/dashboard')
def dashboard(u=Depends(current_user)):return {'donors':len(donors),'available_donors':sum(d['available'] for d in donors),'open_requests':sum(r['status']=='open' for r in requests),'urgent_requests':sum(r['urgent'] for r in requests if r['status']=='open')}
app.mount('/',StaticFiles(directory='web',html=True),name='web')
