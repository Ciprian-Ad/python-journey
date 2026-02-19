import requests
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Load the variables from .env into the system environment
load_dotenv()
console = Console()

def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
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
get_weather("Brasov")
