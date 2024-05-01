# Task2
1. create database named "website"
```sql
CREATE DATABASE website;
```
2. open "website" DB
```sql
USE website;
```
3. create table inside website DB
```sql
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    follower_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```
4. Image
![Database screenshot](task1.png)
