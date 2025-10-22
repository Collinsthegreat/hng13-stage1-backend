#  HNG13 Stage 1 Backend — String Manipulation API

A simple yet powerful **Django REST Framework API** built for **HNG13 Backend Stage 1**, designed to manipulate and query strings intelligently — including **natural language-based string filtering**.

Deployed live on **Railway**:  
 **[https://web-production-88678.up.railway.app](https://web-production-88678.up.railway.app)**

---

##  Tech Stack

- **Backend Framework:** Django 5 + Django REST Framework  
- **Runtime:** Python 3.10+  
- **Server:** Gunicorn  
- **Database:** PostgreSQL (via `dj-database-url`)  
- **Hosting:** Railway  
- **Version Control:** Git + GitHub  

---

##  Features

 Create and list stored strings  
 Retrieve details of a specific string  
 Filter strings by **natural language query** (e.g. “all single word palindromic strings”)  
 Production-ready configuration (Gunicorn, Railway Postgres, `.env` support)  
 Automated testing with Django’s built-in test runner  

---

## 📡 API Endpoints

### 1️ Create or List Strings
**Endpoint:** `POST /strings/`  
**Example Request:**
```bash
curl -X POST https://web-production-88678.up.railway.app/strings/ \
     -H "Content-Type: application/json" \
     -d '{"string": "madam"}'

Example Response:

{
  "id": 1,
  "string": "madam",
  "is_palindrome": true
}


GET /strings/
Retrieves a list of all stored strings.

2️ String Details

Endpoint: GET /strings/<string_value>
Example:

curl https://web-production-88678.up.railway.app/strings/madam


Response:

{
  "string": "madam",
  "length": 5,
  "is_palindrome": true
}

3️ Filter by Natural Language

Endpoint:
GET /strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings

Example Request:

curl "https://web-production-88678.up.railway.app/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings"


Example Response:

[
  {"string": "madam"},
  {"string": "racecar"}
]

 Local Setup Guide

Follow these steps to set up the project locally:

# 1. Clone the repo
git clone https://github.com/<your-username>/hng13-stage1-backend.git
cd hng13-stage1-backend

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Run server
python manage.py runserver


Visit http://127.0.0.1:8000/strings/
 to test locally.

 Environment Variables
Variable	Description	Example
SECRET_KEY	Django secret key	django-insecure-xyz123
DEBUG	Enable debug mode	True or False
DATABASE_URL	PostgreSQL database connection string	postgres://user:password@host:port/dbname
ALLOWED_HOSTS	Comma-separated list of allowed hosts	web-production-88678.up.railway.app
 Example .env File
SECRET_KEY=django-insecure-abc123xyz
DEBUG=True
DATABASE_URL=postgres://user:password@host:port/dbname
ALLOWED_HOSTS=web-production-88678.up.railway.app,localhost,127.0.0.1

 Running Tests

Run all tests to verify functionality:

python manage.py test


You should see:

Ran 3 tests in 0.02s
OK

Deployment (Railway)

Push your project to GitHub

On Railway, create a New Project → Deploy from GitHub repo

Add environment variables under Settings → Variables:

SECRET_KEY

DEBUG=False

ALLOWED_HOSTS=web-production-88678.up.railway.app

DATABASE_URL (automatically created if PostgreSQL plugin added)

Ensure your Procfile contains:

web: gunicorn core.wsgi --log-file -


Deploy and confirm your app is live.

 Author

Your Name: [Collins The Great]
Email: yourname@example.com

GitHub: github.com/your-username

 License

This project is licensed under the MIT License — feel free to modify and use.
