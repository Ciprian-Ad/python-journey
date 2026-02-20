import requests
from rich.console import Console

console = Console()

def get_weather(city):
    #this is a public test API that return dummy data
    url = f"https://jsonplaceholder.typicode.com/posts/1"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        console.print(f"[bold green] Connected![/bold green] Data received: {data['title']}")
    else:
        console.print(f"[bold red] Failed to connect to the internet![/red] Status code: {response.status_code}")

get_weather("Brasov")