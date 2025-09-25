# main.py
from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db, User, User_Weather, Base, engine, SessionLocal
from auth import user_hash_password, user_verify_password
from weather_api import get_weather, get_5day_forecast
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="SUPERSECRETSESSIONKEY")

# mount static files + templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# startup: create tables and ensure admin user exists
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@gmail.com").first()
        if not admin:
            admin_user = User(
                username="admin",
                email="admin@gmail.com",
                hashed_password=user_hash_password("123"),
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()

# root -> login
@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse(url="/login")

# ---------- AUTH ----------
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    if email.lower() == "admin@gmail.com":
        return templates.TemplateResponse("register.html", {"request": request, "error": "This email is reserved."})
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "User already exists"})
    new_user = User(username=username, email=email, hashed_password=user_hash_password(password))
    db.add(new_user)
    db.commit()
    return templates.TemplateResponse("login.html", {"request": request, "success": "Registered successfully! Please login."})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user_verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    request.session["user_id"] = user.id
    request.session["is_admin"] = bool(user.is_admin)
    if user.is_admin:
        return RedirectResponse(url="/admin_dashboard", status_code=302)
    return RedirectResponse(url="/user_dashboard", status_code=302)

# ---------- USER DASHBOARD ----------
@app.get("/user_dashboard", response_class=HTMLResponse)
def user_dashboard(request: Request, db: Session = Depends(get_db)):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login")
    user = db.query(User).filter(User.id == request.session["user_id"]).first()
    if not user:
        return RedirectResponse(url="/login")
    history = db.query(User_Weather).filter(User_Weather.user_id == user.id).order_by(User_Weather.timestamp.desc()).all()
    return templates.TemplateResponse("user_dashboard.html", {"request": request, "user": user, "history": history})

@app.post("/get_weather", response_class=HTMLResponse)
def get_weather_route(request: Request, city: str = Form(...), db: Session = Depends(get_db)):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login")
    user = db.query(User).filter(User.id == request.session["user_id"]).first()
    if not user:
        return RedirectResponse(url="/login")
    data = get_weather(city)
    forecast = get_5day_forecast(city)
    forecast_days = []
    if forecast and "list" in forecast:
        lst = forecast["list"]
        for i in range(0, min(len(lst), 40), 8):
            forecast_days.append(lst[i])
    if not data:
        history = db.query(User_Weather).filter(User_Weather.user_id == user.id).order_by(User_Weather.timestamp.desc()).all()
        return templates.TemplateResponse("user_dashboard.html", {"request": request, "user": user, "history": history, "error": "City not found or API error"})
    weather_entry = User_Weather(
        user_id=user.id,
        city=city,
        temperature=data["main"]["temp"],
        description=data["weather"][0]["description"],
        humidity=data["main"]["humidity"],
        wind_speed=data["wind"]["speed"]
    )
    db.add(weather_entry)
    db.commit()
    history = db.query(User_Weather).filter(User_Weather.user_id == user.id).order_by(User_Weather.timestamp.desc()).all()
    return templates.TemplateResponse("user_dashboard.html", {"request": request, "user": user, "weather": data, "forecast_days": forecast_days, "history": history})

# ---------- HISTORY ----------
@app.get("/history", response_class=HTMLResponse)
def history_page(request: Request, db: Session = Depends(get_db)):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login")
    user = db.query(User).filter(User.id == request.session["user_id"]).first()
    history = db.query(User_Weather).filter(User_Weather.user_id == user.id).order_by(User_Weather.timestamp.desc()).all()
    return templates.TemplateResponse("history.html", {"request": request, "user": user, "history": history})

# ---------- EDIT PROFILE ----------
@app.get("/edit_profile", response_class=HTMLResponse)
def edit_profile_page(request: Request, db: Session = Depends(get_db)):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login")
    user = db.query(User).filter(User.id == request.session["user_id"]).first()
    return templates.TemplateResponse("edit_profile.html", {"request": request, "user": user})

@app.post("/edit_profile", response_class=HTMLResponse)
def edit_profile(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(None), db: Session = Depends(get_db)):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login")
    user = db.query(User).filter(User.id == request.session["user_id"]).first()
    user.username = username
    user.email = email
    if password:
        user.hashed_password = user_hash_password(password)
    db.commit()
    return RedirectResponse(url="/user_dashboard")

# ---------- USER CRUD ----------
@app.get("/update_weather/{entry_id}", response_class=HTMLResponse)
def update_weather_page(entry_id: int, request: Request, db: Session = Depends(get_db)):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login")
    entry = db.query(User_Weather).filter(User_Weather.id == entry_id).first()
    if not entry:
        return RedirectResponse(url="/user_dashboard")
    return templates.TemplateResponse("weather_entry_update.html", {"request": request, "entry": entry})

@app.post("/update_weather/{entry_id}", response_class=HTMLResponse)
def update_weather(entry_id: int, request: Request, city: str = Form(...), temperature: float = Form(...), description: str = Form(...), timestamp: str = Form(...), db: Session = Depends(get_db)):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login")
    entry = db.query(User_Weather).filter(User_Weather.id == entry_id).first()
    if entry:
        entry.city = city
        entry.temperature = temperature
        entry.description = description
        try:
            entry.timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass
        db.commit()
    return RedirectResponse(url="/user_dashboard")

@app.get("/delete_weather/{entry_id}")
def delete_weather(entry_id: int, request: Request, db: Session = Depends(get_db)):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login")
    entry = db.query(User_Weather).filter(User_Weather.id == entry_id).first()
    if entry:
        db.delete(entry)
        db.commit()
    return RedirectResponse(url="/user_dashboard")

# ---------- ADMIN DASHBOARD ----------
@app.get("/admin_dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/login")
    users_count = db.query(User).count()
    weather_count = db.query(User_Weather).count()
    recent_users = db.query(User).order_by(User.id.desc()).limit(5).all()
    recent_weather = db.query(User_Weather).order_by(User_Weather.timestamp.desc()).limit(10).all()
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "users_count": users_count,
            "weather_count": weather_count,
            "recent_users": recent_users,
            "recent_weather": recent_weather,
            "users": db.query(User).all()
        }
    )

# ---------- ADMIN USERS PAGE ----------
@app.get("/admin/users", response_class=HTMLResponse)
def admin_users_page(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/login")
    users = db.query(User).all()
    return templates.TemplateResponse("admin_users.html", {"request": request, "users": users})

# ---------- ADMIN WEATHER PAGE ----------
@app.get("/admin/weather", response_class=HTMLResponse)
def admin_weather_page(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/login")
    entries = db.query(User_Weather).order_by(User_Weather.timestamp.desc()).all()
    return templates.TemplateResponse("admin_weather.html", {"request": request, "entries": entries})

# ---------- ADMIN EDIT PROFILE ----------
@app.get("/admin/edit_profile", response_class=HTMLResponse)
def admin_edit_profile_page(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/login")
    admin_user = db.query(User).filter(User.id == request.session["user_id"]).first()
    return templates.TemplateResponse("admin_edit_profile.html", {"request": request, "user": admin_user})

@app.post("/admin/edit_profile", response_class=HTMLResponse)
def admin_edit_profile(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(None), db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/login")
    admin_user = db.query(User).filter(User.id == request.session["user_id"]).first()
    admin_user.username = username
    admin_user.email = email
    if password:
        admin_user.hashed_password = user_hash_password(password)
    db.commit()
    return RedirectResponse(url="/admin_dashboard")

# ---------- ADMIN CRUD ----------
@app.get("/admin/update_weather/{entry_id}", response_class=HTMLResponse)
def admin_update_weather_page(entry_id: int, request: Request, db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        raise HTTPException(status_code=403, detail="Access denied")
    entry = db.query(User_Weather).filter(User_Weather.id == entry_id).first()
    if not entry:
        return RedirectResponse(url="/admin/weather")
    return templates.TemplateResponse("weather_entry_update.html", {"request": request, "entry": entry, "admin": True})

@app.post("/admin/update_weather/{entry_id}", response_class=HTMLResponse)
def admin_update_weather(entry_id: int, request: Request, city: str = Form(...), temperature: float = Form(...), description: str = Form(...), timestamp: str = Form(...), db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        raise HTTPException(status_code=403, detail="Access denied")
    entry = db.query(User_Weather).filter(User_Weather.id == entry_id).first()
    if entry:
        entry.city = city
        entry.temperature = temperature
        entry.description = description
        try:
            entry.timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass
        db.commit()
    return RedirectResponse(url="/admin/weather")

@app.get("/admin/delete_weather/{entry_id}")
def admin_delete_weather(entry_id: int, request: Request, db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        raise HTTPException(status_code=403, detail="Access denied")
    entry = db.query(User_Weather).filter(User_Weather.id == entry_id).first()
    if entry:
        db.delete(entry)
        db.commit()
    return RedirectResponse(url="/admin/weather")

# ---------- LOGOUT ----------
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)

