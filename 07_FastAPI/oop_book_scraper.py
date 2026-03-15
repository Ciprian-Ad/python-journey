import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
# --- 1. The Data Object ---
class Book:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    # This is a special Python method. It tells Python how to print this object cleanly!
    def __str__(self):
        return f"📕 {self.title} - {self.price}"

    def to_dict(self):
        """Converts the Book object into a dictionary, which is useful for DataFrames."""
        # Keep only digits and the decimal point
        clean_price_string = ''.join(char for char in self.price if char.isdigit() or char == '.')
        return {
            'Title': self.title,
            'Price': float(clean_price_string)  # Convert the cleaned price string to a float
        }
# --- 2. The Scraper Engine ---
class BookScraper:
    def __init__(self, base_url, total_pages=1):
        self.base_url = base_url
        self.total_pages = total_pages
        self.scraped_books = []  # This will hold our Book objects!

    def run(self):
        """The main method to run the scraper."""
        for page in range(1, self.total_pages + 1):
            self.target_url = f"{self.base_url}catalogue/page-{page}.html"
            html_content = self.fetch_page()
            if html_content:
                self.parse_books(html_content)
            time.sleep(1)  # Be polite and wait a bit before the next request
        

    def fetch_page(self):
        """Downloads the raw HTML from the target URL."""
        print(f"🌐 Fetching data from: {self.target_url}")
        response = requests.get(self.target_url)
        
        # 🛑 THE FIX: Force the correct encoding before reading the text!
        response.encoding = 'utf-8'
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.text
        else:
            print(f"❌ Failed to fetch page. Status code: {response.status_code}")
            return None

    def parse_books(self, html_content):
        """Hunts through the HTML to find books and turns them into Python Objects."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Hint 1: Find all <article> tags with the class "product_pod"
        book_articles = soup.find_all('article', class_='product_pod')
        # Hint 2: Loop through them.
        for article in book_articles:
            # Hint 3: Extract the title (from the <h3> tag's <a> element) 
            book_title = article.find('h3').find('a')['title']  # Extract the title
            # Hint 4: Extract the price (from the <p class="price_color"> element)
            book_price = article.find('p', class_='price_color').text  # Extract the price
            # Hint 5: Create a new Book(title, price) object and append it to self.scraped_books
            book = Book(book_title, book_price)
            self.scraped_books.append(book)
            
    def display_results(self):
        """Prints out all the books we found."""
        print(f"\n📚 Successfully scraped {len(self.scraped_books)} books:")
        for book in self.scraped_books:
            print(book) # This automatically uses our __str__ method from the Book class!

    def export_to_csv(self, filename="books.csv"):
        """Converts the scraped objects into a DataFrame and saves to CSV."""
        # 1. Convert our list of Book objects into a list of dictionaries
        book_dictionaries = [book.to_dict() for book in self.scraped_books]
        
        # 2. Load it into Pandas
        df = pd.DataFrame(book_dictionaries)
        
        # 3. Save it!
        df.to_csv(filename, index=False)
        print(f"💾 Successfully saved {len(df)} books to {filename}!")
        
        # Bonus: Print out some instant Data Analysis!
        print(f"💰 The average book price is: £{df['Price'].mean():.2f}")

# --- 3. Let's run it! ---
if __name__ == "__main__":
    # Initialize our scraping robot
    my_scraper = BookScraper(base_url="http://books.toscrape.com/", total_pages=5)  #
    my_scraper.run()  # This will run the whole scraping process, including fetching, parsing, displaying, and exporting results!
    my_scraper.display_results()
    my_scraper.export_to_csv()
