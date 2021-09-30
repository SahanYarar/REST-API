## RestApi

- [What is this project ?](https://github.com/SahanYarar/REST-API#what-is-this-project-)
- [HTTP Verbs](https://github.com/SahanYarar/REST-API#http-verbs)
- [Request and Response Examples](https://github.com/SahanYarar/REST-API#request-and-response-examples)
- [Schemas of User and Account](https://github.com/SahanYarar/REST-API#schemas-of-user-and-account)
- [HTTP Status Codes](https://github.com/SahanYarar/REST-API#http-status-codes)
- [Testing Codes](https://github.com/SahanYarar/REST-API#testing-codes)

### What is this project ?
This project is simple example of  Rest-API with sqlalchemy,pytest and marshmallow .It has  user and account modules.User can take 6 values but 4 of them given as default.Default values are id,created_at,updated_at and is_admin.Account takes five values, three of these given as default.
Default values for admin are id,created_at and updated_at.User and account are linked by one to many method.For example one user can have 3 accounts but one account can't have 2 users.




### HTTP Verbs

| HTTP METHOD |POST   | GET         | DELETE    | PUT  |          
| ------------| ------|-------------|------------- | ------------- | 
| Crud OP     |CREATE |READ    |DELETE       | UPDATE       | 
| /users      | /create_user   | /{user_id}  |/delete/{user_id} | /update/{user_id}| 
|/accounts    |/create_account |/{account_id}|/delete/{account_id} |/update/{account_id}|






## Request and Response Examples
1. User Examples
     - [POST /users/create_user](https://github.com/SahanYarar/REST-API#post-userscreate_user)
     - [PUT /users/update/{user_id}](https://github.com/SahanYarar/REST-API#put-usersupdateuser_id)
     - [GET /users/{user_id}](https://github.com/SahanYarar/REST-API#get-usersuser_id)
     
    
2. Account Examples
     - [POST /accounts/create_account](https://github.com/SahanYarar/REST-API#post-accountscreate_account)
     - [PUT /accounts/update/{account_id}](https://github.com/SahanYarar/REST-API#put-accountsupdateaccount_id)
     
    
## User Examples    
### POST /users/create_user
*Created_at* and *is_admin* are given by default when you create  user object  
Request body:
```
{
    "email": "sahan@hotmail.com",
    "username": "Sahan"
}
```
Response body:
```
{
    "email": "sahan@hotmail.com",
    "id": 1,
    "is_admin": false,
    "username": "Sahan"
}
```
### PUT users/update/{user_id}
If you use the user update function, the value updated_at is set by default

Request body:

```
{
    "is_admin":true
}
```
Response body:
```
{
    "created_at": 2021-08-19T19:40:02.621649+03:00,
    "email": "sahan@hotmail.com",
    "id": 1,
    "is_admin": true,
    "updated_at": "2021-09-01T16:53:39.686296+03:00",
    "username": "Sahan"
}
```
### GET users/{user_id}

Response body:
```
{
    "created_at": "2021-08-19T19:40:02.621649+03:00",
    "email": "sahan@hotmail.com",
    "id": 1,
    "is_admin": false,
    "updated_at": "2021-08-19T19:42:02.621649+03:00",
    "username": "Sahan"
}
```
## Account Examples
### POST /accounts/create_account
Request Body:
```
{
   "name":"Sahass",
   "user_id":"1"
}
```
Response Body:
```
{
    "created_at": "2021-08-18T15:16:41.682799+03:00",
    "id": 1,
    "name": "Sahass",
    "updated_at": "2021-08-18T15:16:41.682799+03:00",
    "user_id": 1
}
```
### PUT /accounts/update/{account_id}
Request Body:
```
{
    "name":"sahan",
    "user_id":"2"
}
```
Response Body:
```
{
    "created_at": "2021-08-18T15:16:41.682799+03:00",
    "id": 1,
    "name": "sahan",
    "updated_at": "2021-09-02T11:26:10.675547+03:00",
    "user_id": 2
}
```
## Schemas of User and Account
```
from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(validate=validate.Length(max=20))
    email = fields.Email(validate=validate.Length(max=120))
    is_admin = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class AccountSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=validate.Length(max=20))
    user_id = fields.Integer()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
```
## HTTP Status Codes
- 200 -OK
- 201 -Created 
- 204 -Deleted
- 400 -Bad Request
- 404 -NotFound
## Examples
### Good request for update:
```
{
    "email":"sahan@hotmail.com",
    "username":"Sahan",
    "is_admin":true
}
```
Status Code: 200

### Bad request for update:
```
{
    "email":"sahanhotmail.com",
    "username":"Sahan",
    "is_admin":true
}
```
Response:
```
{
    "message": "Given value or values are wrong{'email': ['Not a valid email address.']}"
}
```
Status Code : 400

## Testing Codes
You can improve and test your codes.For example:
```
import string
import pytest
from app import app
from db import init_test_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def database():
    try:
        db = init_test_db()
        yield db
    finally:
        db.close_all()
        
def test_create_user(client, database):
    response = client.post('/users/create_user', json={"username": "test_username", "email": "test@gmail.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "test_username"
    assert data["is_admin"] == False
    response1 = client.post('/users/create_user', json={"email": "test@gmail.com"})
    assert response1.status_code == 201
    data1 = response1.get_json()
    assert data1["username"] == "Sahan"
    assert data1["email"] == "test@gmail.com"
    # bad_scenarios
    response2 = client.post('/users/create_user', json={"username": "test_username"})
    assert response2.status_code == 400
    response3 = client.post('/users/create_user', json={"username": "test_username", "email": "testgmail.com"})
    assert response3.status_code == 400        
```




