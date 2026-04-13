from  .utils import *
from ..routers.users import get_current_user, get_db
from fastapi import status

import pytest

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]= override_get_current_user



def test_return_user(test_user):
    response= client.get("/users")
    assert response.status_code==status.HTTP_200_OK
    assert response.json()['username'] == 'achraf'
    assert response.json()['email'] == 'codingwithAchraf'
    assert response.json()['first_name'] == 'Achraf'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(111)-111-1111'

def test_change_password_success(test_user):
    response=client.put("/users/password",json={"password":"testpass",
                                               "new_password":"newpassword"})
    assert response.status_code== status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response=client.put("/users/password", json={"password":"wrong",
                                               "new_password":"newpassword"})
    assert response.status_code== status.HTTP_401_UNAUTHORIZED
    assert response.json() =={'detail':'Verification failed'}

def test_phone_number_change(test_user):
    response= client.put("/users/phone_number/2222222222")
    assert response.status_code== status.HTTP_204_NO_CONTENT
    