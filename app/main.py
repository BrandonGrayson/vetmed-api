from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from .config import settings
from psycopg2.extras import RealDictCursor
from . import utils, oauth2, schemas


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
    print('database connection successful')
except Exception as error:
    print("connection to database failed")
    print("Error", error)


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def root(user: schemas.User):

    hashed_password = utils.hash_password(user.password)

    user.password = hashed_password

    cur.execute("INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *",
                (user.email, user.password))
    user_details = cur.fetchone()
    conn.commit()
    return user_details


@app.post('/login')
async def login(user_credentials: schemas.User):
    cur.execute('SELECT * FROM users WHERE email = (%s)',
                (user_credentials.email,))
    user = cur.fetchone()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify_password(user_credentials.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user['id']})

    return {"access_token": access_token, "token_type": "bearer"}


@app.post('/medications', status_code=status.HTTP_201_CREATED)
def add_medication(medication: schemas.Medication, user_id: int = Depends(oauth2.get_current_user)):

    cur.execute("INSERT INTO medications (name, description, used_for, dont_take_with, user_id) VALUES (%s, %s, %s, %s, %s) RETURNING * ",
                (medication.name, medication.description, medication.used_for, medication.dont_take_with, user_id))
    new_med = cur.fetchone()

    if not new_med:
        raise HTTPException(status_code=404, detail="Item not found")

    conn.commit()

    return new_med


@app.get('/medications')
async def get_medications(user_id: int = Depends(oauth2.get_current_user)):
    cur.execute("SELECT * FROM medications WHERE user_id=(%s)", (user_id,))

    medications = cur.fetchall()

    return medications
