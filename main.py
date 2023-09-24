from typing import Union
from fastapi import FastAPI
from AIModel import analyzeCV, generateCodeSnippet
from dotenv import dotenv_values
from pymongo import MongoClient
from pydantic import BaseModel

config = dotenv_values(".env")
app = FastAPI()

@app.on_event("startup")
def startup_db_client():
  app.mongodb_client = MongoClient(config["DATABASE_URL"])
  app.database = app.mongodb_client[config["DB_NAME"]]
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
    new_user = app.database.users.insert_one(user)
    print("User created")
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
  

@app.post("/generateCode")
async def generateCode(promt: str):
  try:
    analyzed_cv = generateCodeSnippet(promt)
    print("Code generated")
    return analyzed_cv
  except:
    print("Error generating code")
    return "ERROR"