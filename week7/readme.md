# Connect FastAPI with MySQL DB
1. make sure the SQL is up and running
```terminal
sudo /usr/local/mysql/support-files/mysql.server start
```
```terminal
mysql -u root -p
```
```
uvicorn week7.main:app --reload
```
2. testing api response
two options: terminal using curl and postman
curl
    - run the app
    - open up another terminal
    - curl -X GET "http://127.0.0.1:8000/api/member?account=111" -H "accept: application/json"
    - check the response e.g. {"response":{"id":1,"name":"111","account":"111"}}
postman
    - download the app
    - GET method 
    - check in the api route e.g. http://127.0.0.1:8000/api/member?account=ppp
    - check the response
        {
            "response": {
                "id": 14,
                "name": "Pikachu",
                "account": "ppp"
            }
        }
