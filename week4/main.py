from fastapi import FastAPI, Request, Form #run app via fastapi, request from user input via form
from urllib.parse import quote # quote specific message in the URL
from fastapi.staticfiles import StaticFiles # serve static files from static folder
from fastapi.templating import Jinja2Templates #render pre-defined html in templates folder
from fastapi.responses import RedirectResponse #redirect to another URL
import uvicorn # run app on specific host and port
from pydantic import BaseModel #record logic of account and password
from starlette.middleware.sessions import SessionMiddleware #record session

app = FastAPI()

# Configure session middleware with a secret key
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
# Mount static folder at /static URL path
app.mount("/static", StaticFiles(directory="static"), name="static") 
# render pre-defined html in templates folder
templates = Jinja2Templates(directory="templates")

class LoginRequest(BaseModel): 
    account: str
    password: str

# verification logic set account and password to "test"
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
        #once verified, set SIGNED-IN state to TRUE
        request.session['signed_in'] = True
        return RedirectResponse(url="/member", status_code=303)
    else: 
        error_message = quote("Username or password is not correct")
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

# Success page - Redirect 
@app.get("/member")
async def success_page(request: Request):
    if request.session.get('signed_in'):
        return templates.TemplateResponse("success.html", {"request": request, "data": "Successful login!"})
    else:
        return RedirectResponse(url="/", status_code=303)

@app.get("/error")
async def error_page(request: Request):
    error_message = request.query_params.get("message", "自訂的錯誤訊息") # Get message from query string
    return templates.TemplateResponse("error.html", {"request": request, "error_message": error_message}) 

@app.get("/signout") #get method
async def signout(request: Request):
    request.session['signed_in'] = False
    return RedirectResponse(url="/", status_code=303)

#error handling
#@app.exception_handler(Exception)  
#async def error_handler(request: Request, exc: Exception):
#    error_message = request.query_params.get("message", "自訂的錯誤訊息")  # Get message from query string
#    return templates.TemplateResponse("error.html", {"request":request, "error_message": error_message})  

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
