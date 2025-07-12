
# ATS-CV Generator API

API for generating ATS proof resumes

## 🖇 Index

- [🛠 Technologies and Infrastructure](#technologies-and-infrastructure)
- [🧩 API Reference](#api-reference)
- [🌐 Run Locally](#run-locally)
- [🧪 Running Tests](#running-tests)

## 🛠 Technologies and Infrastructure

**Design:** Domain Driven Design + Clean Architecture

**Development:** Test Driven Development

**Tech:** Python, FastAPI, PostgreSQL, Docker


## 🧩 API Reference

### Check health

```http
  GET /api/health/
```

200 Successful Response | Response body
```json
{
  "detail": "ok"
}
```

### Register new User

```http
  POST /api/users/register/
```

Request body
```json
{
  "first_name": "string",
  "late_name": "string",
  "email_address": "user@example.com",
  "password": "string"
}
```

201 Successful Response | Example Value
Schema
```json
{
  "detail": {
    "message": "User successfully registered"
  },
  "data": {
    "user_id": 1,
    "access_token": null,
    "description": [
      {
        "first_name": "string",
        "last_name": "string",
        "email_address": "user@example.com",
        "created_at": "string",
      },
    ],
  },
}
```

### Login User

```http
  POST /api/users/login/
```

Request body
```json
{
  "email_address": "user@example.com",
  "password": "string"
}
```

200 Successful Response | Example Value
Schema
```json
{
  "detail": {
    "message": "Login successful"
  },
  "data": {
    "user_id": 1,
    "access_token": "string",
    "description": [
      {
        "first_name": "string",
        "last_name": "string",
        "email_address": "user@example.com",
        "created_at": "string",
      },
    ],
  },
}
```

### Create new CV

```http
  POST /api/cvs/create/
```

> [!NOTE]
> Requires JWT authentication. Send the token in the header: Authorization: Bearer <token>

Request body
```json
{
    "first_name": "string",
    "last_name": "string",
    "email_address": "string",
    "phone_number": "string",
    "linkedin_url": "string",
    "portfolio_url": "string",
    "country": "string",
    "city": "string",
    "summary": "string",
}
```

201 Successful Response | Example Value
Schema
```json
{
  "detail": {
    "message": "Cv created succesfully"
  },
  "data": {
    "cv_id": 0,
    "user_id": 0,
    "description": [
      {
        "first_name": "string",
        "last_name": "string",
        "email_address": "string",
        "phone_number": "string",
        "linkedin_url": "string",
        "portfolio_url": "string",
        "country": "string",
        "city": "string",
        "summary": "string",
      },
    ],
  },
}
```

### Create new Work Experience

```http
  POST /api/cvs/work-experience/
```

> [!NOTE]
> Requires JWT authentication. Send the token in the header: Authorization: Bearer <token>

Request body
```json
{
  "cv_id": 0,
  "work_experiences": [
      {
      "role": "string",
      "company_name": "string",
      "summary": "string",
      "start_date": "2025-06-24",
      "end_date": "2025-06-24",
    },
  ],
}
```

201 Successful Response | Example Value
Schema
```json
{
  "detail": {
    "message": "Work Experiences saved succesfully"
  },
  "data": {
    "cv_id": 0,
    "user_id": 0,
    "description": [
      {
        "role": "string",
        "company_name": "string",
        "summary": "string",
        "start_date": "2025-06-24",
        "end_date": "2025-06-24"
      },
    ],
  },
}
```

### Create new Education

```http
  POST /api/cvs/education/
```

> [!NOTE]
> Requires JWT authentication. Send the token in the header: Authorization: Bearer <token>

Request body
```json
{
  "cv_id": 0,
  "educations": [
      {
        "title": "string",
        "institution": "string",
        "start_date": "2025-06-24",
        "end_date": "2025-06-24",
      },
  ],
}
```

201 Successful Response | Example Value
Schema
```json
{
  "detail": {
    "message": "Educations saved succesfully"
  },
  "data": {
    "cv_id": 0,
    "user_id": 0,
    "description": [
      {
        "title": "string",
        "institution": "string",
        "start_date": "2025-06-24",
        "end_date": "2025-06-24"
      },
    ],
  },
}
```

### Create new Courses

```http
  POST /api/cvs/courses/
```

> [!NOTE]
> Requires JWT authentication. Send the token in the header: Authorization: Bearer <token>

Request body
```json
{
  "cv_id": 0,
  "courses": [
      {
        "title": "string",
        "institution": "string",
        "start_date": "2025-06-24",
      },
  ],
}
```

201 Successful Response | Example Value
Schema
```json
{
  "detail": {
    "message": "Courses saved succesfully"
  },
  "data": {
    "cv_id": 0,
    "user_id": 0,
    "description": [
      {
        "title": "string",
        "institution": "string",
        "start_date": "2025-06-24",
      },
    ],
  },
}
```

### Create new Skill

```http
  POST /api/cvs/skills/
```

> [!NOTE]
> Requires JWT authentication. Send the token in the header: Authorization: Bearer <token>

Request body
```json
{
  "cv_id": 0,
  "skills": [
      "string",
      "string",
  ],
}
```

201 Successful Response | Example Value
Schema
```json
{
  "detail": {
    "message": "Skills saved succesfully"
  },
  "data": {
    "cv_id": 0,
    "user_id": 0,
    "description": [
      "string",
      "string",
    ],
  },
}
```

## 🌐 Run Locally

Clone the project

```bash
  git clone https://github.com/Leo-a-silva/ATS-CV-generator-BACK.git
```

Switch to the 'develop' branch
```bash
  git checkout develop
```

Create a new “.env” file using your credentials to connect to a PostgreSQL database
```bash
  DB_USERNAME=your-username
  DB_PASSWORD=your-password
  DB_HOST=your-host
  DB_PORT=your-port
  DB_NAME=your-database-name
```

Start the server using Docker Compose

```bash
  docker compose up --build
```


## 🧪 Running Tests

> [!WARNING]  
> The tests implemented are specifically designed to run in a development environment. Each test deletes the records from the database once it is executed. Do not run the tests in a production environment.

Create a new virtual environment
```bash
  python -m venv venv
  source venv/bin/activate
```

Install dependencies
```bash
  pip install -r requirements.txt
```

Run all tests
```bash
  cd src
  python -m pytest
```

Run specific test file
```bash
  python -m pytest path/to/the/file.py
```

Run specific test function
```bash
  python -m pytest path/to/the/file.py -k "test_function"
```

