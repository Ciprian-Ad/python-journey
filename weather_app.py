import requests
import os
import plotext as plt
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

# Load the variables from .env into the system environment
load_dotenv()
console = Console()
api_key = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    with console.status(f"[bold green] Fetching weather data for {city}...[/bold green]") as status:
        response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        desc = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']

        #Creating a rich table to display the weather data
        #  
        weather_info = (
            f"🌡️  [bold]Temperature:[/bold] {temp}°C\n"
            f"☁️  [bold]Condition:[/bold] {desc.capitalize()}\n"
            f"💧 [bold]Humidity:[/bold] {humidity}%\n"
            f"💨 [bold]Wind Speed:[/bold] {wind} m/s"
        )

        console.print(Panel(weather_info, title=f"Weather in {city}", border_style="bold yellow"))
    else:
        console.print(f"[bold red] Failed to fetch weather data for {city}![/bold red] Status code: {response.status_code}")
        console.print(response.json())

def get_7_day_forecast(city):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geo_res = requests.get(geo_url).json()
    if not geo_res:
        console.print(f"[bold red] City '{city}' not found![/bold red]")
        return None
    
    lat, lon = geo_res[0]['lat'], geo_res[0]['lon']
    
    weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    data = requests.get(weather_url).json()
    
    # Extract temperatures (taking one reading per day)
    daily_data = data['list'][::8] # [::8] skips 24 hours (8 * 3h)

    temps = [item['main']['temp'] for item in daily_data]
    timestamps = [item['dt_txt'].split(" ")[0] for item in daily_data]
    
    return temps, timestamps

# Main Execution
cities = []
while len(cities) < 3:
    name = input(f"Enter city {len(cities)+1}: ")
    cities.append(name)

plt.clf() # Clear any previous plots
plt.theme("dark") # Give it a professional dark look
plt.title("5-Day Temperature Forecast")
plt.ylabel("Temperature (°C)")
plt.xlabel("Date")
plt.date_form("Y-m-d") # Tell plotext how to read your strings

for city in cities:
    temp_data, time_data = get_7_day_forecast(city)
    if temp_data:
        plt.plot(time_data, temp_data, label=city, marker="fhd")# Add city data to the plot

plt.xticks(time_data) # Force the dates to show up on the axis
plt.show() # Render the chart in terminal