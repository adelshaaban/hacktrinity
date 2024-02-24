from fastapi import FastAPI

app = FastAPI()

@app.get("/api")
async def get_serever_status():
    return "Server is running successfully"