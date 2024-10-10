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

This diagram shows the relationships between the tables in the library system:

![Database Diagram](https://dbdiagram.io/e/67083c1d97a66db9a3973e73/67083c2897a66db9a3973f32)

### API Documentation

## Authentication API

### **POST** `/auth/signup`

- **Description:** Sign up a new user (librarian or member).
- **Request Body:**
  - `username`: String (required)
  - `password`: String (required)
  - `first_name`: String (required)
  - `last_name`: String (required)
  - `role`: String (LIBRARIAN/MEMBER)
- **Success Response:**
  - Code: 201
  - Content: `{"message": "User created successfully"}`
- **Error Responses:**
  - Code: 400
  - Content: `{"error": "Username already exists"}`

---

### **POST** `/auth/login`

- **Description:** Login for users to get an access token.
- **Request Body:**
  - `username`: String (required)
  - `password`: String (required)
- **Success Response:**
  - Code: 200
  - Content: `{"access_token": "<JWT_TOKEN>", "user_role": "<USER_ROLE>"}`
- **Error Responses:**
  - Code: 400
  - Content: `{"error": "User does not exist"}` (if user is deleted)
  - Code: 400
  - Content: `{"error": "Invalid password"}` (if the password is incorrect)

---

## Librarian API

### **GET** `/librarian/books`

- **Description:** Get a list of all books.
- **Access:** Requires librarian login.
- **Success Response:**
  - Code: 200
  - Content: `[{"id": 1, "title": "Book Title", ...}]`
- **Error Responses:**
  - Code: 403
  - Content: `{"error": "Access forbidden: Librarian role required"}`

---

### **POST** `/librarian/add_book`

- **Description:** Add a new book to the library.
- **Access:** Requires librarian login.
- **Request Body:**
  - `title`: String (required)
  - `author`: String (required)
  - `published_year`: String (optional)
- **Success Response:**
  - Code: 201
  - Content: `{"message": "Book added successfully"}`
- **Error Responses:**
  - Code: 400
  - Content: `{"error": "Invalid request data"}`

---

### **DELETE** `/librarian/delete_book`

- **Description:** Delete a book from the library.
- **Access:** Requires librarian login.
- **Request Body:**
  - `book_id`: Integer (required)
- **Success Response:**
  - Code: 200
  - Content: `{"message": "Book deleted successfully"}`
- **Error Responses:**
  - Code: 400
  - Content: `{"error": "Book ID is required"}`

---

### **PUT** `/librarian/update_book`

- **Description:** Update details of an existing book.
- **Access:** Requires librarian login.
- **Request Body:**
  - `book_id`: Integer (required)
  - `title`: String (optional)
  - `author`: String (optional)
  - `published_year`: String (optional)
- **Success Response:**
  - Code: 200
  - Content: `{"message": "Book updated successfully"}`
- **Error Responses:**
  - Code: 400
  - Content: `{"error": "Book ID is required"}`

---

### **POST** `/librarian/add_member`

- **Description:** Add a new library member.
- **Access:** Requires librarian login.
- **Request Body:**
  - `username`: String (required)
  - `password`: String (required)
  - `first_name`: String (required)
  - `last_name`: String (required)
- **Success Response:**
  - Code: 201
  - Content: `{"message": "Member created successfully"}`
- **Error Responses:**
  - Code: 400
  - Content: `{"error": "Username already exists"}`

---

### **DELETE** `/librarian/delete_member`

- **Description:** Soft delete a member.
- **Access:** Requires librarian login.
- **Request Body:**
  - `member_id`: Integer (required)
- **Success Response:**
  - Code: 200
  - Content: `{"message": "Member deleted successfully"}`
- **Error Responses:**
  - Code: 400
  - Content: `{"error": "Member ID is required"}`

---

### **PUT** `/librarian/update_member`

- **Description:** Update a member's details.
- **Access:** Requires librarian login.
- **Request Body:**
  - `member_id`: Integer (required)
  - `username`: String (optional)
  - `first_name`: String (required)
  - `last_name`: String (required)
- **Success Response:**
  - Code: 200
  - Content: `{"message": "Member updated successfully"}`
- **Error Responses:**
  - Code: 400
  - Content: `{"error": "Member ID is required"}`

---

### **GET** `/librarian/member_history`

- **Description:** View a member's borrowing history.
- **Access:** Requires librarian login.
- **Query Parameters:**
  - `member_id`: Integer (required)
- **Success Response:**
  - Code: 200
  - Content: `[{"book_id": 1, "borrowed_date": "YYYY-MM-DD", ...}]`
- **Error Responses:**
  - Code: 400
  - Content: `{"error": "Member ID is required"}`

---

### **GET** `/librarian/view_members`

- **Description:** View all library members.
- **Access:** Requires librarian login.
- **Success Response:**
  - Code: 200
  - Content: `[{"id": 1, "username": "john_doe", ...}]`
- **Error Responses:**
  - Code: 403
  - Content: `{"error": "Access forbidden: Librarian role required"}`

---

## Member API

### **GET** `/member/available_books`

- **Description:** View a list of available books to borrow.
- **Access:** Requires member login.
- **Success Response:**
  - Code: 200
  - Content: `[{"id": 1, "title": "Book Title", ...}]`
- **Error Responses:**
  - Code: 403
  - Content: `{"error": "Access forbidden: Member role required"}`

---

### **POST** `/member/borrow_book`

- **Description:** Borrow a book.
- **Access:** Requires member login.
- **Request Body:**
  - `book_id`: Integer (required)
- **Success Response:**
  - Code: 200
  - Content: `{"message": "Book borrowed successfully"}`
- **Error Responses:**
  - Code: 400
  - Content: `{"error": "Book ID is required"}`

---

### **POST** `/member/return_book`

- **Description:** Return a borrowed book.
- **Access:** Requires member login.
- **Request Body:**
  - `book_id`: Integer (required)
- **Success Response:**
  - Code: 200
  - Content: `{"message": "Book returned successfully"}`
- **Error Responses:**
  - Code: 400
  - Content: `{"error": "Book ID is required"}`

---

### **DELETE** `/member/delete_account`

- **Description:** Delete the member's account.
- **Access:** Requires member login.
- **Success Response:**
  - Code: 200
  - Content: `{"message": "Account deleted successfully"}`
- **Error Responses:**
  - Code: 400
  - Content: `{"error": "Return all books before deleting account"}`

---

### **GET** `/member/books_borrowed`

- **Description:** View a list of books borrowed by the member.
- **Access:** Requires member login.
- **Success Response:**
  - Code: 200
  - Content: `[{"book_id": 1, "borrowed_date": "YYYY-MM-DD", ...}]`
- **Error Responses:**
  - Code: 403
  - Content: `{"error": "Access forbidden: Member role required"}`


### Hosting Instructions

## PythonAnywhere Setup:

1. Sign up an account on PythonAnywhere.
2. Create a new web app and select the Flask framework.
3. Clone your repository into the PythonAnywhere file system.
4. Set up a virtual environment and install the required packages from `requirements.txt`.
5. Configure the web app to point to your Flask application.

## Environment Variables:

Set up environment variables in the `.env` file. Ensure `SQLALCHEMY_DATABASE_URI`, `JWT_SECRET_KEY`, and other necessary variables are correctly set.

## Database Migration:

Run the following commands to set up the database:
```sh
flask db migrate
flask db upgrade
```

## Running the Application:
Start the web app from the PythonAnywhere dashboard. Ensure the application is running correctly by visiting the provided URL.