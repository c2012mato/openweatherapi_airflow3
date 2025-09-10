from __future__ import annotations

import os
from datetime import datetime, timezone
import logging
from airflow.sdk import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

import pendulum
import requests

# Retrieve API key from environment variable
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# List of Asian capital cities with coordinates
ASIA_CAPITAL_CITIES = [
    {"name": "Kabul", "lat": 34.52, "lon": 69.17},
    {"name": "Yerevan", "lat": 40.17, "lon": 44.50},
    {"name": "Baku", "lat": 40.38, "lon": 49.89},
    {"name": "Manama", "lat": 26.22, "lon": 50.58},
    {"name": "Dhaka", "lat": 23.71, "lon": 90.41},
    {"name": "Thimphu", "lat": 27.47, "lon": 89.63},
    {"name": "Bandar Seri Begawan", "lat": 4.89, "lon": 114.94},
    {"name": "Phnom Penh", "lat": 11.55, "lon": 104.92},
    {"name": "Beijing", "lat": 39.91, "lon": 116.40},
    {"name": "Nicosia", "lat": 35.17, "lon": 33.37},
    {"name": "Tbilisi", "lat": 41.72, "lon": 44.78},
    {"name": "New Delhi", "lat": 28.61, "lon": 77.21},
    {"name": "Jakarta", "lat": -6.20, "lon": 106.82},
    {"name": "Tehran", "lat": 35.69, "lon": 51.39},
    {"name": "Baghdad", "lat": 33.34, "lon": 44.39},
    {"name": "Jerusalem", "lat": 31.77, "lon": 35.22},
    {"name": "Tokyo", "lat": 35.69, "lon": 139.69},
    {"name": "Amman", "lat": 31.95, "lon": 35.93},
    {"name": "Nur-Sultan", "lat": 51.17, "lon": 71.43},
    {"name": "Kuwait City", "lat": 29.37, "lon": 47.98},
    {"name": "Bishkek", "lat": 42.87, "lon": 74.60},
    {"name": "Vientiane", "lat": 17.97, "lon": 102.61},
    {"name": "Beirut", "lat": 33.89, "lon": 35.50},
    {"name": "Kuala Lumpur", "lat": 3.14, "lon": 101.69},
    {"name": "Malé", "lat": 4.17, "lon": 73.51},
    {"name": "Ulaanbaatar", "lat": 47.92, "lon": 106.92},
    {"name": "Naypyidaw", "lat": 19.76, "lon": 96.08},
    {"name": "Kathmandu", "lat": 27.72, "lon": 85.32},
    {"name": "Pyongyang", "lat": 39.03, "lon": 125.75},
    {"name": "Muscat", "lat": 23.61, "lon": 58.59},
    {"name": "Islamabad", "lat": 33.72, "lon": 73.04},
    {"name": "Ramallah", "lat": 31.90, "lon": 35.20},
    {"name": "Manila", "lat": 14.60, "lon": 120.98},
    {"name": "Doha", "lat": 25.29, "lon": 51.53},
    {"name": "Moscow", "lat": 55.75, "lon": 37.62},
    {"name": "Riyadh", "lat": 24.71, "lon": 46.68},
    {"name": "Singapore", "lat": 1.35, "lon": 103.82},
    {"name": "Seoul", "lat": 37.57, "lon": 126.98},
    {"name": "Sri Jayawardenepura Kotte", "lat": 6.93, "lon": 79.86},
    {"name": "Damascus", "lat": 33.51, "lon": 36.31},
    {"name": "Taipei", "lat": 25.03, "lon": 121.57},
    {"name": "Dushanbe", "lat": 38.56, "lon": 68.77},
    {"name": "Bangkok", "lat": 13.75, "lon": 100.50},
    {"name": "Dili", "lat": -8.56, "lon": 125.57},
    {"name": "Ankara", "lat": 39.93, "lon": 32.86},
    {"name": "Ashgabat", "lat": 37.95, "lon": 58.38},
    {"name": "Abu Dhabi", "lat": 24.45, "lon": 54.38},
    {"name": "Tashkent", "lat": 41.29, "lon": 69.24},
    {"name": "Hanoi", "lat": 21.03, "lon": 105.85},
    {"name": "Sana'a", "lat": 15.37, "lon": 44.21}
]
 
@dag(
    dag_id="weather_etl_dag",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    doc_md="""
    ### Weather ETL DAG

    This DAG fetches weather data for major Asian capital cities and stores it in a PostgreSQL database.
    It uses dynamic task mapping to fetch weather for each city in parallel.
    This DAG is not scheduled and must be triggered manually.
    """,
)
def weather_etl_dag():
    """
    This DAG defines the ETL process for fetching and storing weather data.
    """
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="postgres",
        sql="""
        CREATE TABLE IF NOT EXISTS weather (
            id SERIAL PRIMARY KEY,
            city VARCHAR(255),
            country VARCHAR(255),
            temperature FLOAT,
            humidity INTEGER,
            wind_speed FLOAT,
            weather_description VARCHAR(255),
            date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    
    @task
    def fetch_weather(city: dict) -> dict:
        """
        Fetches current weather data for a given city from the OpenWeatherMap API.
        """
        lat = city["lat"]
        lon = city["lon"]
        city_name = city["name"]
        
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        return {
            "city": city_name,
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "date": datetime.now(timezone.utc).date().isoformat()
        }

    @task
    def store_weather_data(weather_data_list: list[dict]):
        """
        Connects to PostgreSQL and stores a list of weather data using PostgresHook.insert_rows.
        """
        pg_hook = PostgresHook(postgres_conn_id="postgres")
        
        # Define the target table and columns for the insert
        target_table = "weather"
        target_fields = ["city", "temperature", "humidity", "weather_description", "date"]
        
        # Transform the list of dictionaries into a list of tuples
        rows_to_insert = [
            (
                weather["city"],
                weather["temperature"],
                weather["humidity"],
                weather["description"],
                weather["date"]
            )
            for weather in weather_data_list
        ]
        
        if not rows_to_insert:
            logging.info("No weather data to insert.")
            return

        logging.info(f"Inserting {len(rows_to_insert)} rows into {target_table}...")
        pg_hook.insert_rows(
            table=target_table,
            rows=rows_to_insert,
            target_fields=target_fields
        )
        logging.info("Insertion complete.")


    # Dynamically create a fetch_weather task for each city
    weather_data = fetch_weather.expand(city=ASIA_CAPITAL_CITIES)
    
    # A single task to store all the fetched weather data
    store_task = store_weather_data(weather_data_list=weather_data)
    
    # Define the task dependencies
    create_table >> weather_data >> store_task

# Instantiate the DAG
weather_etl_dag()