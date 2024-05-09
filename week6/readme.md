# Connect FastAPI with MySQL DB
1. pip install mysql-connector-python
2. change MySQL DB password 
reference by ![https://jennyttt.medium.com/reset-mysql-root-password-on-mac-d767d0cc6e29]
3. Create table users
```sql
SHOW DATABASES;
USE website;
SHOW TABLES;
DESCRIBE users;
```
*to start the fastapi
```
uvicorn week6.main:app --reload
```
4. create table inside website DB
```sql
CREATE TABLE message (
    id BIGINT AUTO_INCREMENT PRIMARY KEY, 
    member_id BIGINT UNSIGNED NOT NULL, -- UNSIGNED
    FOREIGN KEY(member_id) REFERENCES users (id), -- reference to users table's 'id'
    content VARCHAR(255) NOT NULL, 
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);
```
5. update message member_id to reference user table on id
```sql
ALTER TABLE message
MODIFY COLUMN member_id BIGINT;

ALTER TABLE message
ADD CONSTRAINT member_id
  FOREIGN KEY (member_id)
  REFERENCES users(id);
```