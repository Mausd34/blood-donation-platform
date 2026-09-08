from fastapi.testclient import TestClient
from api import app
client=TestClient(app)
def test_health(): assert client.get('/health').status_code==200
def test_donor():
    r=client.post('/donors',json={'name':'Demo Donor','blood_group':'O+','city':'Dhaka','phone':'demo','available':True})
    assert r.status_code==200
    assert client.get('/donors?blood_group=O+').status_code==200
