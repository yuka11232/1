import sqlite3
from datetime import datetime
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('weather.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime TEXT,
        temperature REAL
    )
''')
conn.commit()


def fetch_current_temperature():
    url = 'https://www.timeanddate.com/weather/azerbaijan/baku'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    temp_element = soup.find('div', class_='h2')
    temperature = temp_element.text.strip().replace('°C', '')
    return float(temperature)

try:
    temperature = fetch_current_temperature()
except Exception as e:
    print(f"Error fetching temperature: {e}")
    temperature = None


if temperature is not None:
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO weather_data (datetime, temperature)
        VALUES (?, ?)
    ''', (current_datetime, temperature))
    conn.commit()
    print(f"Data inserted: {current_datetime}, Temperature: {temperature}°C")
else:
    print("Temperature data not available; skipping database insertion.")


conn.close()
