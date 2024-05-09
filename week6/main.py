from fastapi import FastAPI, Request, Form, Depends #run app via fastapi, request from user input via form
from urllib.parse import quote, parse_qs # quote specific message in the URL
from fastapi.staticfiles import StaticFiles # serve static files from static folder
from fastapi.templating import Jinja2Templates #render pre-defined html in templates folder
from fastapi.responses import RedirectResponse, HTMLResponse #redirect to another URL
import uvicorn # run app on specific host and port
from pydantic import BaseModel #record logic of account and password
from starlette.middleware.sessions import SessionMiddleware #record session
import mysql.connector #connect with MySQL DB

app = FastAPI()

# Configure session middleware with a secret key
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
# Mount static folder at /static URL path
app.mount("/static", StaticFiles(directory="week6/static"), name="static") 
# render pre-defined html in templates folder
templates = Jinja2Templates(directory="week6/templates")

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

def get_member_details(request: Request, account: str):
    database_connection(db_config)
    try:
      # Establish database connection (assuming combined logic from previous examples)
      db_connection = mysql.connector.connect(**db_config)

      if not db_connection:
          return None  # Error establishing connection

      # Create a cursor
      db_cursor = db_connection.cursor()

      if account:  # Username provided (initial login scenario)
          # Define the query to retrieve details by username
          query = "SELECT id, account, name FROM users WHERE account = %s"
          db_cursor.execute(query, (account,))
      else:  # No username provided (use session data)
          # Get member ID from the session (assuming called from within a route handler)
          member_id = request.session.get("member_id")
          if not member_id:
              return None  # No member ID found in session

          # Define the query to retrieve details by member ID
          query = "SELECT id, account, name FROM users WHERE id = %s"
          db_cursor.execute(query, (member_id,))

      # Fetch the first result
      result = db_cursor.fetchone()

      if result:
          # Return the user details as a tuple
          return result
      else:
          # User not found
          return None

    except mysql.connector.Error as e:
        print(f"Error fetching user details: {e}")
        return None

    finally:
        # Close the cursor and connection (handled by the combined logic)
        pass

def insert_message(member_id: int, content: str):
    if not content:
        error_message = "Content cannot be empty"
        print(error_message)  # Print the error message for debugging purposes
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
'''
def delete_message_by_id(id: int):    
    # Configure the database connection
    db_connection = database_connection(db_config)   
    if not db_connection:
        raise Exception("Database connection error")
    try:
        with db_connection.cursor() as db_cursor:
            # Execute a query to delete the message
            query = "DELETE FROM message WHERE id = %s"
            db_cursor.execute(query, (id,))

        # Commit the transaction
        db_connection.commit()

    except mysql.connector.Error as e:
        # Handle any database errors
        print(f"Error deleting message: {e}")

    finally:
        pass
'''

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
        #record member_id, username, name
        if user_details:
            #record details in the session
            #once verified, set SIGNED-IN state to TRUE
            request.session['signed_in'] = True
            request.session["id"] = user_details[0]
            request.session["account"] = user_details[1]
            request.session["name"] = user_details[2]

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
        # Create a cursor
        with db_connection.cursor() as db_cursor:
            # Execute a query to fetch messages with user IDs
            query = "SELECT id, member_id, content FROM message ORDER BY TIME DESC"
            db_cursor.execute(query)
            messages_data = db_cursor.fetchall()

            # Iterate over the messages to fetch user names
            for message_data in messages_data:
                message = {}
                message['id'] = message_data[0]
                message['content'] = message_data[2]

                # Fetch the user name based on member_id
                user_query = "SELECT name FROM users WHERE id = %s"
                db_cursor.execute(user_query, (message_data[1],))
                user_data = db_cursor.fetchone()

                if user_data:
                    message['user_name'] = user_data[0]
                else:
                    message['user_name'] = "Unknown"

                messages.append(message)

    except mysql.connector.Error as e:
        # Handle any database errors
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

'''
@app.post("/deleteMessage") #delete message via post method
async def delete_message(request: Request):
    message_id = request.form.get("id")
    if not message_id:
        error_message = quote("Message ID not found in request")
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

    # Delete the message from the database
    delete_message_by_id(message_id)

    # Redirect back to the member page
    return RedirectResponse(url="/member", status_code=303)
'''
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
