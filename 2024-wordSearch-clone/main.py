from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List
import mysql.connector
import hashlib
import jwt
import datetime

secret_key = "mysecretkey"

# MySQL 연결 설정
db = mysql.connector.connect(
    host="localhost", user="root", password="1111", database="word_search"
)


class Signup(BaseModel):
    nickname: str
    email: EmailStr
    password: str


class Login(BaseModel):
    email: EmailStr
    password: str


class Signin(BaseModel):
    email: EmailStr
    password: str


class GameInfo(BaseModel):
    title: str
    description: str
    words: List[str]
    accessToken: str


class UpdateGameInfo(BaseModel):
    url: str
    gameId: int


class VerifyWord(BaseModel):
    gameId: int
    word: str


app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # 클라이언트로부터 메시지 수신
        data = await websocket.receive_text()
        print(f"Received message from client: {data}")
        # 메시지를 다시 클라이언트에게 전송
        await websocket.send_text(f"Message received: {data}")


async def generateJWT(email, user_id):
    # 현재 시간을 UTC 기준으로 가져오기
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    # 만료 시간 설정 (현재 시간에서 1주일 후로 설정)
    expiration_time = now_utc + datetime.timedelta(weeks=1)
    payload = {"email": email, "user_id": user_id, "exp": expiration_time}
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    print("token", token)
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
            "nickname": result[3],
        }
        return user_info
    else:
        return None


async def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


async def verify_token(token: str):
    decode_token = jwt.decode(token, secret_key, algorithms=["HS256"])

    return decode_token["user_id"]


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.post("/signup")
async def signup(request: Request, user: Signup):
    if is_email_duplicate(user.email):
        return JSONResponse(content={"detail": "Email already exists"}, status_code=400)
    hashed_password = await hash_password(user.password)
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password, nickname) VALUES (%s, %s, %s)",
            (user.email, hashed_password, user.nickname),
        )
        db.commit()
        return JSONResponse(
            content={"message": "User created successfully"}, status_code=201
        )
    except mysql.connector.Error as err:
        return JSONResponse(content={"error": str(err)}, status_code=500)


@app.post("/signin")
async def signin(request: Request, user: Signin):
    try:
        hashed_password = await hash_password(user.password)
        find_users = await find_users_by_email(user.email)
        if find_users and hashed_password == find_users["password"]:
            access_token = await generateJWT(find_users["email"], find_users["id"])
            return JSONResponse(
                content={
                    "message": "User Login successfully",
                    "access_token": access_token,
                },
                status_code=200,
            )
        else:
            return JSONResponse(
                content={"error": "Invalid email or password"}, status_code=401
            )
    except mysql.connector.Error as err:
        return JSONResponse(content={"error": str(err)}, status_code=500)


@app.post("/save_game_info")
async def save_game_info(game_info: GameInfo):
    cursor = db.cursor()
    try:
        user_id = await verify_token(game_info.accessToken)
        # 게임 정보를 games 테이블에 저장
        cursor.execute(
            "INSERT INTO games (title, description ,create_user_id) VALUES (%s, %s ,%s)",
            (game_info.title, game_info.description, user_id),
        )
        db.commit()
        # 새로 생성된 게임의 id 가져오기
        game_id = cursor.lastrowid
        # 게임의 단어들을 words 테이블에 저장
        for word in game_info.words:
            cursor.execute(
                "INSERT INTO words (word, game_id) VALUES (%s, %s)", (word, game_id)
            )
        db.commit()
        game_url = f"http://localhost:5173/#/game/{game_id}"
        return JSONResponse(
            content={
                "message": "Game information saved successfully",
                "game_url": game_url,
            },
            status_code=200,
        )
    except mysql.connector.Error as err:
        db.rollback()
        return JSONResponse(content={"error": str(err)}, status_code=500)


@app.put("/update_game_info_for_url")
async def update_game_info_for_url(update_game_info: UpdateGameInfo):
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE games SET url = %s WHERE id = %s",
            (update_game_info.url, update_game_info.gameId),
        )
        db.commit()
        return JSONResponse(content={"message": "Updated game URL"}, status_code=201)
    except mysql.connector.Error as err:
        return JSONResponse(content={"error": str(err)}, status_code=500)


@app.get("/get_game_info/{gameId}")
async def get_game_info(gameId: int):
    cursor = db.cursor(dictionary=True)
    try:
        # Fetch game info and related words using a JOIN query
        cursor.execute(
            """
            SELECT games.id, games.title, games.description, games.create_user_id, games.url,
            games.created_at, words.id as word_id, words.word
            FROM games
            LEFT JOIN words ON games.id = words.game_id
            WHERE games.id = %s
        """,
            (gameId,),
        )

        # Extract game information and words from the result set
        game_info = {}
        for row in cursor.fetchall():
            if not game_info:
                game_info = {
                    "id": row["id"],
                    "title": row["title"],
                    "description": row["description"],
                    "create_user_id": row["create_user_id"],
                    "url": row["url"],
                    "created_at": str(row["created_at"]),
                    "words": [],
                }
            if row["word_id"] is not None:
                game_info["words"].append({"id": row["word_id"], "word": row["word"]})

        # Return JSON response
        if game_info:
            return JSONResponse(
                content={
                    "message": "Game information is available",
                    "game_info": game_info,
                },
                status_code=200,
            )
        else:
            return JSONResponse(
                content={"message": "Game information is not available"},
                status_code=404,
            )
    except mysql.connector.Error as err:
        return JSONResponse(content={"error": str(err)}, status_code=500)


@app.post("/verify-word")
async def verify_word(data: VerifyWord):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM words WHERE game_id = %s AND word = %s",
            (data.gameId, data.word),
        )
        word_recode = cursor.fetchone()
        if word_recode:
            return JSONResponse(content={"correct": True, "message": "Correct word"},status_code=201)
    except mysql.connector.Error as err:
        return JSONResponse(
            content={"correct": False, "error": str(err)}, status_code=500)
