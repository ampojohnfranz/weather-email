import requests
import smtplib
import os
import logging
from email.message import EmailMessage
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from config import LAT, LON, RAIN_THRESHOLD
from email_builder import build_html

# Setup
load_dotenv()
logging.basicConfig(
    filename="weather.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

API_KEY    = os.environ.get("OPENWEATHER_KEY")
EMAIL      = os.environ.get("EMAIL")
APP_PASS   = os.environ.get("APP_PASSWORD")
RECIPIENT  = os.environ.get("RECIPIENT", EMAIL)

PHT   = timezone(timedelta(hours=8))
now   = datetime.now(PHT)
today = now.date()
today_text = now.strftime("%d %B %Y (%A)")

# Fetch
try:
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    )
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    logging.error(f"API fetch failed: {e}")
    raise SystemExit("Weather fetch failed. Check weather.log.")

# Current Weather (add this after the forecast fetch)
try:
    current_url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    )
    current_response = requests.get(current_url, timeout=10)
    current_response.raise_for_status()
    current_data = current_response.json()
    current_temp = current_data["main"]["temp"]
    current_condition = current_data["weather"][0]["description"].title()
except Exception as e:
    logging.warning(f"Current weather fetch failed: {e}")
    current_temp = None
    current_condition = "Unavailable"

# Parse
rows_today = []
for row in data.get("list", []):
    dt_pht = datetime.strptime(row["dt_txt"], "%Y-%m-%d %H:%M:%S") \
             .replace(tzinfo=timezone.utc).astimezone(PHT)
    if dt_pht.date() == today:
        rows_today.append((dt_pht, row))

if not rows_today:
    logging.warning("No forecast rows found for today.")
    raise SystemExit("No data for today.")

max_rain_prob = 0.0
peak_rain_time = "N/A"
peak_temp = -99.0
total_rain_mm = 0.0

for dt_pht, row in rows_today:
    prob = row.get("pop", 0) * 100
    if prob > max_rain_prob:
        max_rain_prob = prob
        peak_rain_time = dt_pht.strftime("%I:%M %p")

    temp = row["main"]["temp"]
    if temp > peak_temp:
        peak_temp = temp

    total_rain_mm += row.get("rain", {}).get("3h", 0)

# Status
if max_rain_prob >= RAIN_THRESHOLD:
    status = "Rain Expected"
    advice = "Bring an umbrella."
else:
    status = "Low Rain Probability"
    advice = "Weather conditions are optimal."

# Build + Send
html = build_html(today_text, status, current_temp, current_condition, max_rain_prob, peak_rain_time, now)

msg = EmailMessage()
msg["Subject"] = f"Weather Brief — {status} | {now.strftime('%d %b')}"
msg["From"]    = EMAIL
msg["To"]      = RECIPIENT
msg.set_content("Open in an HTML-supported email client.")
msg.add_alternative(html, subtype="html")

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, APP_PASS)
        server.send_message(msg)
    logging.info("Email sent successfully.")
    print("Done.")
except Exception as e:
    logging.error(f"Email failed: {e}")
    raise SystemExit("Email send failed. Check weather.log.")