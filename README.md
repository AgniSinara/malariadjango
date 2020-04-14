# malariadjango

## HOW TO RUN
### 1. Install all requirements
```
pip install r requirements.txt
```

### 2. Migrations
```
python manage.py makemigrations
python manage.py migrate
```

### 3. Run Server
```
python manage.py runserver
```
## Additional Information
### Admin Dashboard
> url: 127.0.0.1:8000/admin  
> username: admin  
> password: admin

## API Endpoint
### 1. Register
#### Request
```
POST /api/register

data: 
{
    "username": "patient3",
    "password": "passwordpatient3",
    "firstName": "Nakano",
    "lastName": "Ichika",
    "userType": 3
}
```
#### Response
```
{
  "status": 1,
  "message": "User successfully created"
}
```
##### userType
- 1 = Dokter<br>
- 2 = Tenaga Medis<br>
- 3 = Pasien

### 2. Login
#### Request
```
POST /api/login

data:
{
    "username": "patient3",
    "password": "passwordpatient3"
}
```
#### Response
```
{
  "token": "d2c7ee899087a75f71448dcb93ffee571387b16e",
  "userId": 5,
  "username": "patient3",
  "userType": "Pasien"
}
```
Any further request will need a token provided in the authorization header for authentication.


### 3. Get My Profile
#### Request
```
GET /api/me

header
{
    "Authorization": "d2c7ee899087a75f71448dcb93ffee571387b16e"
}
```
#### Response
```
{
  "username": "patient3",
  "fullName": "Nakano Ichika",
  "userType": 3
}
```


### 4. Get All Patient
#### Request
```
GET /api/patients

header
{
    "Authorization": "d2c7ee899087a75f71448dcb93ffee571387b16e"
}
```
#### Response
```
{
  "status": 1,
  "patientData": [
    {
      "id": 3,
      "username": "patient1",
      "fullName": "nakano miku",
      "userType": 3
    },
    {
      "id": 5,
      "username": "patient3",
      "fullName": "Nakano Ichika",
      "userType": 3
    }
  ]
}
```