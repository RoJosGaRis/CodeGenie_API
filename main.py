from typing import Union
from fastapi import FastAPI
from AIModel import analyzeCV, generateCodeSnippet
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

config = dotenv_values(".env")
app = FastAPI()

origins = [
    "http://localhost:3000",  # Replace with your frontend's URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True,  # Set this to True if you need to allow cookies or authentication headers
)

@app.on_event("startup")
def startup_db_client():
  
  app.mongodb_client = MongoClient(config["DATABASE_URL"], server_api = ServerApi('1'))
  app.database = app.mongodb_client[config["DB_NAME"]]
  app.mycol = app.database["usermodels"]
  print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
  app.mongodb_client.close()

@app.get("/")
def read_root():
  return analyzeCV('I am a software developer with 5 years of experience.')

class User(BaseModel):
  name: str
  email: str
  password: str

@app.post("/create")
async def create_user(user: User):
  try:
    print(user.email)
    new_user = app.database["usermodels"].insert_one(user)
    return new_user
  except:
    print("Error creating user")
    return "ERROR"
  
class CV(BaseModel):
  text: str

@app.post("/analyzeCV")
async def analyze_cv(cv: CV):
  try:
    analyzed_cv = analyzeCV(cv.text)
    print("CV analyzed")
    return analyzed_cv
  except:
    print("Error analyzing CV")
    return "ERROR"
  

class Code(BaseModel):
  languages: str
  skills: str
  tools: str

@app.post("/generateCode")
async def generateCode(promt: Code):
  try:
    analyzed_cv = generateCodeSnippet(promt.languages, promt.skills, promt.tools)
    print("Code generated")
    return analyzed_cv
  except:
    print("Error generating code")
    return "ERROR"