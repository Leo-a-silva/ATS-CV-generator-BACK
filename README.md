
# ATS-CV Generator API

API for generating ATS proof resumes


## Technologies and Infrastructure

**Design:** Domain Driven Design + Clean Architecture

**Development:** Test Driven Development

**Tech:** Python, FastAPI, PostgreSQL, Docker


## API Reference

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
  "email_address": "user@example.com",
  "password": "string"
}
```

201 Successful Response | Example Value
Schema
```json
{
  "user_id": 0,
  "email_address": "string",
  "created_at": "2025-06-24T17:27:04.153Z"
}
```

### Create new CV

```http
  POST /api/cvs/create/
```

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
  "user_id": 0
}
```

201 Successful Response | Example Value
Schema
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
  "cv_id": 0,
  "user_id": 0
}
```

### Create new Work Experience

```http
  POST /api/cvs/work-experience/
```

Request body
```json
[
  {
    "role": "string",
    "company_name": "string",
    "summary": "string",
    "start_date": "2025-06-24",
    "end_date": "2025-06-24",
    "cv_id": 0
  },
]
```

201 Successful Response | Example Value
Schema
```json
[
  {
    "role": "string",
    "company_name": "string",
    "summary": "string",
    "start_date": "2025-06-24",
    "end_date": "2025-06-24"
  },
]
```

### Create new Education

```http
  POST /api/cvs/education/
```

Request body
```json
[
  {
    "title": "string",
    "institution": "string",
    "start_date": "2025-06-24",
    "end_date": "2025-06-24",
    "cv_id": 0
  }
]
```

201 Successful Response | Example Value
Schema
```json
[   
  {
    "title": "string",
    "institution": "string",
    "start_date": "2025-06-24",
    "end_date": "2025-06-24"
  }
]
```
## Run Locally

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


## Running Tests

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

Run tests
```bash
  cd src
  python -m pytest
```

