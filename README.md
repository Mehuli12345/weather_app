Weather App

A modern, full-featured weather web application built with FastAPI, SQLAlchemy, and OpenWeather APIs, featuring user and admin dashboards, history tracking, and real-time weather forecasts.

🔹 Features

User Authentication & Authorization

Secure registration and login with hashed passwords.

Admin user with elevated privileges.

Session-based authentication using SessionMiddleware.

User Dashboard

Search current weather by city.

View 5-day forecast.

Track and manage your weather search history.

Edit profile with optional password update.

Admin Dashboard

Manage all users and weather records.

Edit or delete weather entries.

View recent users and recent weather searches.

Admin profile management.

Weather API Integration

Real-time weather data using OpenWeatherMap API.

Temperature, description, humidity, and wind speed.

5-day forecast in 8-hour intervals.

Database Management

SQLAlchemy ORM for seamless database interactions.

SQLite database for easy local setup.

Auto-creates tables on startup.

Tracks user-specific weather searches with timestamps.

User-Friendly Interface

Beautiful HTML templates with Jinja2.

Clean, responsive design for dashboards and forms.

🔹 Technologies Used

Backend: FastAPI, Python 3.10+

Database: SQLAlchemy, SQLite

Frontend: Jinja2 Templates, HTML/CSS

APIs: OpenWeatherMap API

Authentication: Password hashing, session middleware

Others: Starlette, datetime, Form handling

🔹 Installation & Setup

Clone the repository:

git clone git@github.com:Mehuli12345/weather_app.git
cd weather_app


Create a virtual environment:

python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # Linux/Mac


Install dependencies:

pip install -r requirements.txt


Set up the database & admin user:

Tables are auto-created on startup.

Default admin credentials:

Email: admin@gmail.com

Password: 123

Run the app:

uvicorn main:app --reload


Access the app in your browser:

http://127.0.0.1:8000

🔹 Screenshots

(Add your own screenshots here for login page, user dashboard, admin dashboard, weather search results, etc.)

🔹 Usage

Register as a new user (except admin@gmail.com which is reserved).

Log in and search for weather in any city.

View your weather history and forecast.

Admins can view all users, weather records, and manage entries.

🔹 Project Structure
weather_app/
│
├─ main.py                 # FastAPI routes and app logic
├─ database.py             # SQLAlchemy models and DB setup
├─ auth.py                 # Password hashing and verification
├─ weather_api.py          # API functions for weather and forecast
├─ templates/              # Jinja2 HTML templates
├─ static/                 # CSS, JS, images
└─ requirements.txt        # Python dependencies

🔹 Future Enhancements

Mobile-friendly responsive design.

Dark mode toggle for dashboards.

User profile avatar support.

Deployment to cloud (Heroku / AWS / GCP).

Support for multiple weather APIs for redundancy.

🔹 Contributing

Fork the repo

Create a new branch: git checkout -b feature-name

Commit your changes: git commit -m "Add feature"

Push to branch: git push origin feature-name

Open a pull request

🔹 License

This project is MIT licensed.

🔹 Contact

Developer: Mehuli Lahiri

Email: mehulilahiri84@gmail.com

GitHub: Mehuli12345
