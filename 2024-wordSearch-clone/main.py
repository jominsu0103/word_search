from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel , EmailStr
import mysql.connector
import hashlib
import jwt
import datetime

secret_key = "mysecretkey"

# MySQL 연결 설정
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",
    database="word_search"
)

class Signup(BaseModel):
  nickname:str
  email:EmailStr
  password:str

class Login(BaseModel):
  email:EmailStr
  password:str

class Signin(BaseModel):
  email:EmailStr
  password:str


app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET" ,"POST" ,"DELETE","PUT"],
    allow_headers=["*"],
)

async def generateJWT(email , user_id):
  # 현재 시간을 UTC 기준으로 가져오기
  now_utc = datetime.datetime.now(datetime.timezone.utc)
  
  # 만료 시간 설정 (현재 시간에서 1주일 후로 설정)
  expiration_time = now_utc + datetime.timedelta(hours=1)
  payload = {
    "email" : email,
    "user_id" : user_id,
    "exp": expiration_time
  }
  token = jwt.encode(payload,secret_key,algorithm="HS256")
  print("token",token)
  return token

def is_email_duplicate(email: str) -> bool:
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
    count = cursor.fetchone()[0]
    return count > 0

async def find_users_by_email(email: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    if result:
        user_info = {
            "id": result[0],
            "email": result[1],
            "password": result[2],
            "nickname": result[3]
        }
        return user_info
    else:
        return None


async def hash_password(password:str):
  return hashlib.sha256(password.encode()).hexdigest()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/signup")
async def signup(request: Request , user: Signup):
  if is_email_duplicate(user.email):
    return JSONResponse(content={"detail": "Email already exists"}, status_code=400)
  hashed_password = await hash_password(user.password)
  cursor = db.cursor()
  try:
    cursor.execute("INSERT INTO users (email, password, nickname) VALUES (%s, %s, %s)", (user.email, hashed_password, user.nickname))
    db.commit()
    return JSONResponse(content={"message": "User created successfully"},status_code=201)
  except mysql.connector.Error as err:
    return JSONResponse(content={"error": str(err)}, status_code=500)

@app.post("/signin")
async def signin(request:Request , user:Signin):
  try:
    hashed_password = await hash_password(user.password)
    find_users = await find_users_by_email(user.email)
    if find_users and hashed_password == find_users["password"]:
      access_token = await generateJWT(find_users["email"], find_users["id"])
      return JSONResponse(content = {"message": "User Login successfully", "access_token": access_token} , status_code=200)
    else:
      return JSONResponse(content={"error": "Invalid email or password"}, status_code=401)
  except mysql.connector.Error as err:
    return JSONResponse(content={"error": str(err)}, status_code=500)


