from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel, EmailStr, Field
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

users_db = {} 

class RegisterForm(BaseModel):
    firstname: str = Field(..., min_length=3, description="First name must be at least 3 characters long")
    lastname: str = Field(..., min_length=3, description="Last name must be at least 3 characters long")
    email: EmailStr = Field(..., description="Must be a valid email address")
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")
    confirm_password: str = Field(..., min_length=6, description="Confirm password must match password")

class LoginForm(BaseModel):
    email: EmailStr = Field(..., description="Must be a valid email address")
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")

# Serve the HTML page 

@app.get("/register", response_class=HTMLResponse)
async def register_page():
   with open("register.html", "r", encoding="utf-8") as f:
       return f.read()
   
@app.get("/login", response_class=HTMLResponse)
async def login_page():
    with open("login.html", "r", encoding="utf-8") as f:
        return f.read()
   
@app.post("/register")
async def register(
    firstname: str = Form(...),
    lastname: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)   
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Password and Confirm Password must be same..")
    
    if email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    users_db[email] = {
        "firstname": firstname,
        "lastname": lastname,
        "password": password  
    }
    return {"success": "User registered successfully", "data": users_db[email]}

@app.post("/login")
async def login(
    email: EmailStr = Form(...),
    password: str = Form(...)
):
    user = users_db.get(email)
    if not user:
        raise HTTPException(status_code=400, detail="Email not registered.")
    if user["password"] != password:
        raise HTTPException(status_code=400, detail="Incorrect password.")
    
    return {"success": "Login successful", "data": user}

