from fastapi import FastAPI,UploadFile,File
import uuid

ImagePath = "images/"

app = FastAPI()

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

    return {"filename": file.filename}