from fastapi import FastAPI, Request, Form, Depends, HTTPException, Query, Body #run app via fastapi, request from user input via form
from urllib.parse import quote, parse_qs # quote specific message in the URL
from fastapi.staticfiles import StaticFiles # serve static files from static folder
from fastapi.templating import Jinja2Templates #render pre-defined html in templates folder
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse #redirect to another URL
import uvicorn # run app on specific host and port
from pydantic import BaseModel #record logic of account and password
from starlette.middleware.sessions import SessionMiddleware #record session
import mysql.connector #connect with MySQL DB
from typing import Optional

app = FastAPI()

# Configure session middleware with a secret key
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
# Mount static folder at /static URL path
app.mount("/static", StaticFiles(directory="week7/static"), name="static") 
# render pre-defined html in templates folder
templates = Jinja2Templates(directory="week7/templates")

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rootpass',
    'database': 'website_1'
}

#define the signup request
class SignUpRequest(BaseModel):
    name: str
    account: str
    password: str

#define the memberResponse JSON
class MemberResponse(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    account: Optional[str] = None

#define memberResponse to return None if no input
class QueryResponse(BaseModel):
    data: Optional[MemberResponse]

#define the updateRequest using id and name
class UpdateNameRequest(BaseModel):
    name: str


def database_connection(db_config):
    try:
        # Create a database connection
        db_connection = mysql.connector.connect(**db_config)
        return db_connection
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        return None  # Indicate connection failure

#check if the username exists in the DB
def check_existing_account(account: str):
    # Configure the database connection
    db_connection = database_connection(db_config)
    if db_connection is None:
        return True # prevent duplicate account creation
    try:
        with db_connection.cursor() as db_cursor:
            # Execute a query to check if the account exists
            query = "SELECT * FROM users WHERE account = %s"
            db_cursor.execute(query, (account,))
            # Fetch the result
            result = db_cursor.fetchone()
            if result:
                # Account already exists
                return True
            else:
                # Account does not exist
                return False

    except mysql.connector.Error as e:
        # Handle any database errors
        print(f"Error connecting to the database: {e}")
        return True  #prevent duplicate account creation

    finally:
        # Close the database connection
        db_connection.close()

# verification logic of username and password if matching
def verify_user(account: str, password: str):
    # Configure the database connection
    database_connection(db_config)
    
    try: 
        # Create a database connection
        db_connection = mysql.connector.connect(**db_config)
        # Create a cursor to execute queries -- 
        db_cursor = db_connection.cursor()
    
        # Execute a query to check if the account and password match
        query = "SELECT * FROM users WHERE account = %s AND password = %s"
        db_cursor.execute(query, (account, password))

        # Fetch the result
        result = db_cursor.fetchone()

        if result:
            # User is verified
            return True
        else:
            # User is not verified
            return False
        
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        return False
    
    finally:
        # Close the database connection
        if 'db_connection' in locals():
            db_connection.close()

def insert_user(name: str, account: str, password: str):
    # Configure the database connection
    database_connection(db_config)

    # Check if account already exists
    if check_existing_account(account):
        return "Error: Account already exists"
    
    try:
        # Create a database connection
        db_connection = mysql.connector.connect(**db_config)
        db_cursor = db_connection.cursor()

        # Execute a query to insert the new user
        query = "INSERT INTO users (name, account, password) VALUES (%s, %s, %s)"
        db_cursor.execute(query, (name, account, password))

        # Commit the transaction
        db_connection.commit()

        return "User inserted successfully"

    except mysql.connector.Error as e:
        # Handle any database errors
        print(f"Error connecting to the database: {e}")
        return "Error: Could not insert user"

    finally:
        # Close the database connection
        if 'db_connection' in locals():
            db_connection.close()

def get_member_details(request: Request, account: str = None, user_id: int = None):
    try:
      # Establish database connection
      db_connection = mysql.connector.connect(**db_config)

      if not db_connection.is_connected():
          #print("Error establishing connection")
          return None  # Error establishing connection

      # Create a cursor
      db_cursor = db_connection.cursor()
      #print(f"Initial values - account: {account}, user_id: {user_id}")

      # Retrieve user_id from session if not provided
      if not user_id:
        user_id = request.session.get("member_id")
        #print(f"Retrieved user_id from session: {user_id}")

      if account:  # Username provided
          # Define the query to retrieve details by username
          #print(f"Query by account: {account}")
          query = "SELECT id, account, name FROM users WHERE account = %s"
          db_cursor.execute(query, (account,))
      elif user_id:  # No username provided (use session data)
          #print(f"Query by user_id: {user_id}")
          # Define the query to retrieve details by member ID
          query = "SELECT id, account, name FROM users WHERE id = %s"
          db_cursor.execute(query, (user_id,))
      else: 
          return None

      # Fetch the first result
      result = db_cursor.fetchone()

      if result:
        # Return the user details as a tuple
        print(f"Query result: {result}")
        return result
      else:
        # User not found
        print("User not found")
        return None

    except mysql.connector.Error as e:
        print(f"Error fetching user details: {e}")
        return None

    finally:
        pass

def query_member_details(account: str)->Optional[MemberResponse]:
    database_connection(db_config)
    try:
      db_connection = mysql.connector.connect(**db_config)

      if not db_connection:
          return None  # Error establishing connection

      # Create a cursor
      with db_connection.cursor(dictionary=True) as db_cursor:
          # Define the query to retrieve details by username
          query = "SELECT id, account, name FROM users WHERE account = %s"
          db_cursor.execute(query, (account,))
          # Fetch the first result
          result = db_cursor.fetchone()

      if result:
          return MemberResponse(**result)
      else:
          # User not found
          return None

    except mysql.connector.Error as e:
        print(f"Error fetching user details: {e}")
        return None

    finally:
        pass

def insert_message(member_id: int, content: str):
    if not content:
        error_message = "Content cannot be empty"
        #print(error_message)  # Print the error message for debugging purposes
        return error_message  # Return the error message to the caller
    
    # Configure the database connection
    db_connection = database_connection(db_config)
    try:
        with db_connection.cursor() as db_cursor:
        # Execute a query to insert the new user
            query = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
            db_cursor.execute(query, (member_id, content))

        # Commit the transaction
        db_connection.commit()

        return "Message inserted successfully"

    except mysql.connector.Error as e:
        # Handle any database errors
        print(f"Error connecting to the database: {e}")
        return "Error: Could not insert message"

    finally:
        # Close the database connection
        db_connection.close()

def get_current_user(request: Request) -> Optional[MemberResponse]:
    user_id = request.session.get("id")
    #print(f'User ID from session: {user_id}')

    if user_id is None:
        return None

    user_details = get_member_details(request, user_id=user_id)
    #print(f'User details from database: {user_details}')  


    if user_details:
        # Extract relevant data and create MemberResponse object
        #print(f'user id:', user_id)
        #print(user_details)
        return MemberResponse(id=user_details[0], name=user_details[1], account=user_details[2])
    else:
        return None
    
#homepage rendering index.html
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) 

#path after sign up with method POST
@app.post("/signup")
async def signup(request: Request):
    form_data = await request.form()
    name = form_data.get("name")
    account = form_data.get("account")
    password = form_data.get("password")

    if not name or not account or not password:
        error_message = quote("Please enter name, username, and password")
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
    
    if check_existing_account(account):
        error_message = quote("Repeated username")
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
    else:
        if insert_user(name, account, password):
            # Store the user's name in the session
            request.session["name"] = name
            return RedirectResponse(url="/member", status_code=303)
        else:
            error_message = quote("Failed to insert user")
            return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

#path after sign in with method POST
@app.post("/signin")
async def signin(request: Request):
    form_data = await request.form()
    name = form_data.get("name")
    account = form_data.get("account")
    password = form_data.get("password")

    if not account or not password: #set account and password required also on the frontend
        # Redirect to the error page with a custom message if either field is empty
        error_message = quote("Please enter username and password")
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
    
    db_connection = database_connection(db_config)
    if not db_connection:
        # Handle database connection error
        error_message = "Internal server error"
        return templates.TemplateResponse("error.html", {"error_message": error_message})
    
    #check if username exist in the table
    if verify_user(account, password):
        user_details = get_member_details(request, account)
        #print(user_details)
        #record member_id, username, name
        if user_details:
            #record details in the session
            #once verified, set SIGNED-IN state to TRUE
            request.session['signed_in'] = True
            request.session["id"] = user_details[0]
            request.session["account"] = user_details[1]
            request.session["name"] = user_details[2]
            print(f"Session data set: {request.session}")
        # Redirect to successful signin page
        return RedirectResponse(url="/member", status_code=303)
    else: 
        error_message = quote("Username or password is not correct")
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

@app.get("/member",response_class=HTMLResponse)
async def get_messages(request: Request):
    db_connection = database_connection(db_config)
    if not db_connection:
        return templates.TemplateResponse("error.html", {"error_message": "Database connection error"})
   
    messages = []
    try:
        with db_connection.cursor() as db_cursor:
            # Execute a query to fetch messages with user names using JOIN
            query = """
                SELECT m.id, m.member_id, m.content, u.name, u.account
                FROM message m
                JOIN users u ON m.member_id = u.id
                ORDER BY m.time DESC
            """
            db_cursor.execute(query)
            messages = db_cursor.fetchall()

    except mysql.connector.Error as e:
        print(f"Error fetching messages: {e}")
    
    finally:
        # Close the database connection
        if 'db_connection' in locals():
            db_connection.close()

    return templates.TemplateResponse("member.html", {"request": request, "messages": messages})

@app.get("/error")
async def error_page(request: Request):
    error_message = request.query_params.get("message", "自訂的錯誤訊息") # Get message from query string
    return templates.TemplateResponse("error.html", {"request": request, "error_message": error_message}) 

@app.get("/signout") #get method
async def signout(request: Request):
    request.session['signed_in'] = False
    return RedirectResponse(url="/", status_code=303)

@app.post("/createMessage") #create message via post method
async def createMessage(request: Request):
    form_data = await request.form()
    content = form_data["content"]
    member_id = request.session.get("id")
    print(f"Content received: {content}")

    if not member_id:
        error_message = quote ("member ID not found in session")
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

    if insert_message(member_id, content):
        return RedirectResponse(url="/member", status_code=303)
    else:
        error_message = quote("Failed to insert message")
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

@app.post("/deleteMessage")
async def delete_message(message_id: int = Form(...)):
    db_connection = database_connection(db_config)

    try:
        async with db_connection.cursor() as db_cursor:
            # Delete the message from the database
            query = "DELETE FROM message WHERE id = %s"
            await db_cursor.execute(query, (message_id,))
            await db_connection.commit()

        return RedirectResponse(url="/member", status_code=303)

    except Exception as e:
        print(f"Error deleting message: {e}")
        return {"message": "Error deleting message"}


@app.get('/api/member', response_model=MemberResponse)
def read_member(request: Request, username: str = Query(..., alias="username")):
    #to restrict non-signed in users
    session_data = request.session
    if not session_data.get('account', None):
        return  JSONResponse(content={"data": None})
    account = username

    if not account:
        raise  JSONResponse(content={"data": None})

    print(f"Fetching member details for username: {username}")
    
    member = query_member_details(account)
    print(f"Member data: {member}") 

    if member:
        user_data = {
            "id": member.id,
            "name": member.name,
            "username": member.account
        }
        #member_response = MemberResponse(id=member.id, name=member.name, account=member.account)
        print(f"user data: {user_data}") 
        return JSONResponse(content={"data": user_data})
    
    else:
        response = JSONResponse(content={"data": None})
        print(f"Response content: {response.body}")
        return response

@app.patch('/api/member')
def update_member_name(update_request: UpdateNameRequest = Body(...), current_user:Optional[MemberResponse]=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail={"data": None})
    print(f"Current User (from get_current_user): {current_user}") 

    db_connection = None
    cursor = None

    print(f"Request body: {update_request}")

    try:
        db_connection = database_connection(db_config)
        cursor = db_connection.cursor()

        user_id = current_user.id
        #print("Retrieved User Details:", user_id)  

        if not user_id:
            return {"error": True}

        query = "UPDATE users SET name = %s WHERE id = %s"
        cursor.execute(query, (update_request.name, user_id))
        db_connection.commit()
            
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"name": update_request.name, "ok": True}
    except Exception as e:
        db_connection.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)