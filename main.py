from fastapi import FastAPI,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
import uuid

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://172.20.10.2",
    "http://172.20.10.2:5173",
    "*"
]



ImagePath = "images/"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def get_serever_status():
    return "Server is running successfully"

@app.post("/api")
async def create_upload_file(file: UploadFile = File(...)):
    # file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    #save the file
    with open(f"{ImagePath}{file.filename}", "wb") as f:
        f.write(contents)


    return {"file-response": file}