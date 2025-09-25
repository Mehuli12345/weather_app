🌤 Weather App — Your Real-Time Weather Companion

Welcome to Weather App, your sleek and interactive solution for tracking weather around the globe! Built with 💖 using FastAPI, SQLAlchemy, and Jinja2, this project offers a full-featured user and admin dashboard, real-time weather updates, and a 5-day forecast, making it easy to stay ahead of the weather 🌞🌧❄️.

🚀 Features

✨ User Authentication: Secure registration, login, and session management 🔐
🌆 User Dashboard: Search for weather, view 5-day forecast, and track history 📜
👑 Admin Dashboard: Manage users and weather records with full CRUD support 🛠️
🌡 Weather API Integration: Powered by OpenWeatherMap API for accurate data
🗓 History Tracking: Keep a record of all weather searches with timestamps ⏰
✨ Beautiful Templates: Clean and responsive design with Jinja2 ✨

🧠 Tech Stack
Tech	Description
🐍 Python	Programming language
⚡ FastAPI	Modern Python web framework
🧱 SQLAlchemy	ORM for database interactions
🌐 Jinja2	HTML templating
🗄 SQLite	Database storage
🌦 OpenWeatherMap API	Weather & forecast data
🔑 Starlette SessionMiddleware	Session-based authentication
📁 Project Structure
weather_app/
│
├── main.py                  # FastAPI app and routes
├── database.py              # SQLAlchemy models and DB setup
├── auth.py                  # Password hashing & verification
├── weather_api.py           # Weather API functions
├── templates/               # Jinja2 HTML templates
├── static/                  # CSS, JS, images
└── requirements.txt         # Dependencies

🔧 Setup Instructions

Clone the repository

git clone git@github.com:Mehuli12345/weather_app.git
cd weather_app


Create a virtual environment

python -m venv venv
source venv/Scripts/activate   # Windows
# or
source venv/bin/activate       # Linux/Mac


Install dependencies

pip install -r requirements.txt


Run the app

uvicorn main:app --reload


Open in your browser

http://127.0.0.1:8000


Default admin account:

Email: admin@gmail.com

Password: 123

📬 API Endpoints Overview
Method	Endpoint	Description
GET	/	Redirects to login
GET	/register	Registration page
POST	/register	Register a new user
GET	/login	Login page
POST	/login	Authenticate user
GET	/user_dashboard	User weather dashboard
POST	/get_weather	Get weather & forecast
GET	/history	View search history
GET	/admin_dashboard	Admin dashboard
GET	/admin/users	Manage users
GET	/admin/weather	Manage weather entries
✅ Future Improvements

🌍 Dark mode for dashboards
📱 Fully mobile-responsive UI
🧑‍🤝‍🧑 Role-based authentication enhancements
💳 Online API key management and notifications
📊 Interactive weather charts & analytics

💙 Contributing

Pull requests are welcome! For major changes, please open an issue to discuss before submitting.

💌 Acknowledgements

FastAPI & SQLAlchemy Docs

OpenWeatherMap API for weather data

Jinja2 & Starlette for templates and session management

Freepik / Unsplash for placeholder images
