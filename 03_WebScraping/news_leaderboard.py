import requests
from bs4 import BeautifulSoup
from collections import Counter
from rich.console import Console
from rich.table import Table
import time

console = Console()

def get_headlines(url):
    """Fetches headlines from a given URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,ro;q=0.8'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text from common title tags
            return [tag.get_text().strip().lower() for tag in soup.find_all(['h2', 'h3', 'h4', 'a'])]
        else:
            console.print(f"[yellow]Warning: {url} returned status {response.status_code}[/yellow]")
            return []
    except Exception as e:
        console.print(f"[red]Error connecting to {url}: {e}[/red]")
        return []

def create_leaderboard():
    targets = {
        "Digi24": "https://www.digi24.ro/",
        "HotNews": "https://www.hotnews.ro/",
        "G4Media": "https://www.g4media.ro/",
        "Libertatea": "https://www.libertatea.ro/",
        "Stiripesurse": "https://www.stiripesurse.ro/",
        "RomaniaTV": "https://www.romaniatv.net/"
        }
    
    politicians = ["bolojan", "grindeanu", "nicușor dan", "simion", "buzoianu", "savonea"]
    master_counts = Counter()

    for name, url in targets.items():
        console.print(f"🧐 Analyzing [bold cyan]{name}[/bold cyan]...")
        headlines = get_headlines(url)
        
        # Count mentions for this specific site
        site_mentions = []
        for line in headlines:
            for p in politicians:
                if p in line:
                    site_mentions.append(p)
        
        master_counts.update(site_mentions)
        time.sleep(1) # Be a polite scraper

    # Create the Rich Table
    table = Table(title="🏆 News Leaderboard (Total Mentions)", style="bold green")
    table.add_column("Rank", justify="center")
    table.add_column("Personality", style="magenta")
    table.add_column("Total Mentions", justify="right", style="yellow")

    for rank, (name, count) in enumerate(master_counts.most_common(), start=1):
        table.add_row(str(rank), name.capitalize(), str(count))

    console.print(table)

create_leaderboard()