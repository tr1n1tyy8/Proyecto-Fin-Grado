from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
async def users():
    return {"users": ["Alice", "Bob", "Charlie"]}