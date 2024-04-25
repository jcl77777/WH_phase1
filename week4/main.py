from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")  # Mount static folder at /static URL path

# verification logic
def verify_user(username: str, password: str) -> bool:
    pass

@app.get("/")
async def home():
    return {"message": "Welcome to the login page!"}

@app.post("/signin/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}

# Success page - Redirect 
@app.get("/member")
async def member():
    return {"message": "恭喜您，成功登入系統!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
