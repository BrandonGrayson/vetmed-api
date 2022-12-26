from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from .config import settings
from psycopg2.extras import RealDictCursor

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
try:
    conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name,
                            user=settings.database_username, password=settings.database_password, cursor_factory=RealDictCursor)
    cur = conn.cursor()
except Exception as error:
    print("connection to database failed")
    print("Error", error)


class User(BaseModel):
    email: str
    password: str


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def root(user: User):
    print(user)

    cur.execute("INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *",
                (user.email, user.password))
    user_details = cur.fetchone()
    conn.commit()
    return user_details
