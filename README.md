 library-challenge

## Project Documentation

### Table of Contents
1. [Database Structure](#database-structure)
2. [Database Diagram](#database-diagram)
3. [API Documentation](#api-documentation)
4. [Hosting Instructions](#hosting-instructions)

### Database Structure

#### Tables

1. **Users**
    - `id`: Integer, Primary Key
    - `first_name`: String, Not Null
    - `last_name`: String, Not Null
    - `username`: String, Unique, Not Null
    - `password_hash`: String, Not Null
    - `role`: Enum('LIBRARIAN', 'MEMBER'), Not Null
    - `status`: Enum('ACTIVE', 'DELETED'), Default 'ACTIVE'
    - `created_at`: DateTime, Default datetime.now
    - `updated_at`: DateTime, Default datetime.now, On Update datetime.now

2. **Books**
    - `id`: Integer, Primary Key, Auto Increment
    - `title`: String, Not Null
    - `author`: String, Nullable
    - `published_year`: String (4 characters)
    - `status`: Enum('AVAILABLE', 'BORROWED'), Default 'AVAILABLE'
    - `created_at`: DateTime, Default datetime.now
    - `updated_at`: DateTime, Default datetime.now, On Update datetime.now

3. **MemberHistory**
    - `id`: Integer, Primary Key, Auto Increment
    - `member_id`: Integer, Foreign Key (Users.id), Not Null, On Delete CASCADE
    - `book_id`: Integer, Foreign Key (Books.id), Not Null, On Delete CASCADE
    - `action`: Enum('BORROWED', 'RETURNED'), Not Null
    - `action_date`: DateTime, Default datetime.now


### Database Diagram

+-----------------+       +-----------------+       +---------------------+
|     Users       |       |     Books       |       |   MemberHistory     |
+-----------------+       +-----------------+       +---------------------+
| id (PK)         |       | id (PK)         |       | id (PK)             |
| first_name      |       | title           |       | member_id (FK)      |
| last_name       |       | author          |       | book_id (FK)        |
| username (U)    |       | published_year  |       | action              |
| password_hash   |       | status          |       | action_date         |
| role            |       | created_at      |       +---------------------+
| status          |       | updated_at      |
| created_at      |       +-----------------+
| updated_at      |
+-----------------+

