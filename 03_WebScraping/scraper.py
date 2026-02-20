import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

console = Console()

def scrape_quotes():
    url = "https://quotes.toscrape.com/"
    response = requests.get(url)
    
    # Create the soup object
    soup = BeautifulSoup(response.text, "html.parser")
    
    # In HTML, quotes on this site are stored in <div class="quote">
    quotes = soup.find_all("div", class_="quote")
    
    table = Table(title="Famous Quotes", style="magenta")
    table.add_column("Quote", style="green")
    table.add_column("Author", style="cyan")

    for q in quotes:
        # Extract the text from the <span> and <small> tags
        text = q.find("span", class_="text").get_text()
        author = q.find("small", class_="author").get_text()
        table.add_row(text, author, end_section=True)

    console.print(table)

scrape_quotes()