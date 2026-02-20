"""
Weather App Module
==================

This module defines a WeatherStation class that fetches weather forecast data
from the OpenWeatherMap API for a list of cities and displays temperature charts
using the plotext library.

Requirements:
- OPENWEATHER_API_KEY environment variable (loaded from .env file)
- Dependencies: requests, plotext, python-dotenv, rich

Usage:
    Create a WeatherStation instance with a list of cities,
    fetch the weather data, and display the chart.
"""

import requests
import os
import plotext as plt
from dotenv import load_dotenv
from rich.console import Console

console = Console()

class WeatherStation:
    def __init__(self, city_list):
        """Initialize the WeatherStation with a list of cities."""
        load_dotenv()  # Load environment variables from .env file for secure API key storage
        self.api_key = os.getenv("OPENWEATHER_API_KEY")  # Retrieve the OpenWeatherMap API key
        self.cities = city_list  # Store the list of cities to fetch weather for
        self.data_store = {}  # Dictionary to hold weather data for each city, keyed by city name

    def fetch_weather(self):
        """Loop through the cities and fetch weather data for each."""
        for city in self.cities:
            # Fetch geo coordinates and then the forecast data for the city
            self.data_store[city] = self._get_city_data(city)

    def _get_city_data(self, city):
        """Internal helper method to interact with the OpenWeatherMap API."""
        # Step 1: Get the geocoding data for the city to obtain latitude and longitude
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.api_key}"
        geo_res = requests.get(geo_url).json()
        if not geo_res:
            console.print(f"[bold red] City '{city}' not found![/bold red]")
            return None
    
        lat, lon = geo_res[0]['lat'], geo_res[0]['lon']  # Extract lat and lon from the response
    
        # Step 2: Fetch the 5-day weather forecast using the coordinates
        weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        data = requests.get(weather_url).json()
    
        # Step 3: Extract daily temperatures (API provides data every 3 hours, so take one per day)
        daily_data = data['list'][::8]  # [::8] skips to every 24 hours (8 * 3h intervals)
        temps = [item['main']['temp'] for item in daily_data]  # List of temperatures for each day
        timestamps = [item['dt_txt'].split(" ")[0] for item in daily_data]  # List of dates (YYYY-MM-DD)
    
        return {"temps": temps, "timestamps": timestamps}  # Return a dictionary with temps and timestamps

    def display_chart(self):
        """Render the temperature chart using plotext for all cities with available data."""
        plt.clf()  # Clear any previous plots
        plt.theme("dark")  # Set the plot theme to dark
        plt.date_form("Y-m-d")  # Format dates on x-axis as Year-Month-Day
        
        for city, data in self.data_store.items():
            if data:  # Only plot if data was successfully fetched
                plt.plot(data['timestamps'], data['temps'], label=city)  # Plot temperature vs date for each city
        
        plt.show()  # Display the chart

# Example usage of the WeatherStation class
# Create a WeatherStation instance with a list of cities
my_station = WeatherStation(["Brasov", "London", "Tokyo"])
# Fetch weather data for each city
my_station.fetch_weather()
# Display the temperature chart
my_station.display_chart()