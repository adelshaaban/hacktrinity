from fastapi import FastAPI,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
import os
from work_bet_slow import Ergonomy
from fastapi.responses import FileResponse

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://172.20.10.2",
    "http://172.20.10.2:5173",
    "*"
]



ImagePath = "images/"
OutputPath = "edited_video/"
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

    output = Ergonomy.process_video(f'images/{file.filename}',filename=file.filename)
    return {"file_response": file,"file_url": f"http://192.168.137.13:8000/{output}"}

@app.get("/edited_video/{filename}")
async def get_image(filename: str):
    return FileResponse(os.path.join(OutputPath, filename))

