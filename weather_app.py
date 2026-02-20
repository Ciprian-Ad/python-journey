import requests
import os
import plotext as plt
from dotenv import load_dotenv
from rich.console import Console

console = Console()

class WeatherStation:
    def __init__(self, city_list):
        """Initialize the WeatherStation with a list of cities."""
        load_dotenv()  # Load environment variables from .env file
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.cities = city_list
        self.data_store = {} # Dictionary to hold weather data for each city

    def fetch_weather(self):
        """Loop through the cities and fetch weather data for each."""
        for city in self.cities:
            #Fetching geo coords than the forecast data for the city
            self.data_store[city] = self._get_city_data(city)

    def _get_city_data(self, city):
        """Interanl helper to talk to the the API"""
        # Get the geocoding data for the city
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.api_key}"
        geo_res = requests.get(geo_url).json()
        if not geo_res:
            console.print(f"[bold red] City '{city}' not found![/bold red]")
            return None
    
        lat, lon = geo_res[0]['lat'], geo_res[0]['lon']
    
        weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        data = requests.get(weather_url).json()
    
        # Extract temperatures (taking one reading per day)
        daily_data = data['list'][::8] # [::8] skips 24 hours (8 * 3h)

        temps = [item['main']['temp'] for item in daily_data]
        timestamps = [item['dt_txt'].split(" ")[0] for item in daily_data]
    
        return {"temps": temps, "timestamps": timestamps}

    def display_chart(self):
        """Render the plotext chart."""
        plt.clf()
        plt.theme("dark")
        plt.date_form("Y-m-d")
        
        for city, data in self.data_store.items():
            if data:
                plt.plot(data['timestamps'], data['temps'], label=city)
        
        plt.show()

my_station = WeatherStation(["Brasov", "London", "Tokyo"])
my_station.fetch_weather()
my_station.display_chart()