import requests
import time
from bs4 import BeautifulSoup
from collections import Counter
from rich.console import Console
from rich.table import Table

time.sleep(2)  # Sleep for 2 seconds to avoid overwhelming the servers with requests
console = Console()

def analyze_news(url,site_name):
    #1. Fetch the news page
    """Fetches headlines from a given URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,ro;q=0.8'
    }
    #2. Extract the news headlines (assuming they are in <h2> tags)
    headlines = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text from common title tags
            headlines = [tag.get_text().strip().lower() for tag in soup.find_all(['h2', 'h3', 'h4', 'a'])]
        else:
            console.print(f"[yellow]Warning: {url} returned status {response.status_code}[/yellow]")
    except Exception as e:
        console.print(f"[red]Error connecting to {url}: {e}[/red]")

    #3. Simple keyword analysis: Count the most common words in the headlines
    keywords = ["bolojan", "grindeanu", "nicușor dan", "pnl", "psd", "aur", "usr", "război", "economie", "usa", "europa"]

    #check how many times each keyword appears in the headlines
    found_keywords = []
    for headline in headlines:
        for word in keywords:
            if word in headline:
                found_keywords.append(word)
    
    stats = Counter(found_keywords)

    #4. Display the Results
    table = Table(title=f"Topic Mentions on {site_name}", style="bold yellow")
    table.add_column("Keyword", style="cyan")
    table.add_column("Mentions", justify="right", style="magenta")

    for word, count in stats.most_common():
        table.add_row(word.capitalize(), str(count), end_section=True)

    console.print(table)

# Example usage:
analyze_news("https://www.digi24.ro/", "Digi24")
#analyze_news("https://www.antena3.ro/", "Antena3")
analyze_news("https://www.profit.ro/", "Profit")
analyze_news("https://www.romaniatv.net/", "RomaniaTV")
analyze_news("https://www.g4media.ro/", "G4Media")
analyze_news("https://www.hotnews.ro/", "HotNews")
analyze_news("https://www.libertatea.ro/", "Libertatea")
analyze_news("https://www.stiripesurse.ro/", "Stiripesurse")

