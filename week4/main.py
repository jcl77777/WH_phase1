from fastapi import FastAPI, Request, Body, Form
from urllib.parse import quote
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import uvicorn
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")  # Mount static folder at /static URL path

templates = Jinja2Templates(directory="templates")

class LoginRequest(BaseModel): 
    account: str
    password: str

# verification logic
def verify_user(account: str, password: str) -> bool:
    if account == "test" and password == "test":
        return True
    else:
        return False

#homepage rendering index.html
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) 

#path after sign in with method POST
@app.post("/signin")
async def signin(request: Request, account: str = Form(None), password: str = Form(None)):
    if not account or not password:
        # Redirect to the error page with a custom message if either field is empty
        error_message = quote("Please enter username and password")
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
    if verify_user(account, password):
        return RedirectResponse(url="/member", status_code=303)
    else: 
        error_message = quote("Username or password is not correct")
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

# Success page - Redirect 
@app.get("/member")
async def success_page(request: Request):
    return templates.TemplateResponse("success.html", {"request": request, "data": "Successful login!"})  

@app.get("/error")
async def error_page(request: Request):
    error_message = request.query_params.get("message", "自訂的錯誤訊息") # Get message from query string
    return templates.TemplateResponse("error.html", {"request": request, "error_message": error_message}) 

#error handling
#@app.exception_handler(Exception)  
#async def error_handler(request: Request, exc: Exception):
#    error_message = request.query_params.get("message", "自訂的錯誤訊息")  # Get message from query string
#    return templates.TemplateResponse("error.html", {"request":request, "error_message": error_message})  

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
