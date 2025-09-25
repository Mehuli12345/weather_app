import csv
from database import SessionLocal, User_Weather, Base, engine
from datetime import datetime


Base.metadata.create_all(bind=engine)

db = SessionLocal()

csv_path = r"C:\Users\User\Desktop\weather_app\GlobalWeatherRepository.csv"

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      
        city = row.get("City", "Unknown")
        temperature = float(row.get("Temperature", 0))
        description = row.get("WeatherDescription", "N/A")
        timestamp_str = row.get("LastUpdated", "")
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except:
            timestamp = datetime.utcnow()
        
        entry = User_Weather(
            user_id=None,  # No user info from CSV, set to None
            city=city,
            temperature=temperature,
            description=description,
            timestamp=timestamp
        )
        db.add(entry)

db.commit()
db.close()
print("CSV loaded successfully!")
