from fastapi import FastAPI,UploadFile

app = FastAPI()

@app.get("/api")
async def get_serever_status():
    return "Server is running successfully"

@app.post("/api")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}