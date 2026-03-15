from oop_book_scraper import BookScraper, Book
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class NewBook(BaseModel):
    title: str
    price: float
# 1. Initialize the app globally so Uvicorn can find it
app = FastAPI()
#storage for custom books added via the API (not scraped)
custom_books_db = []

# 2. Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Book Scraper API!"}
    
# 3. Scrape endpoint
@app.get("/scrape")
def scrape(pages: int = 5, max_price: float = None):  # Allow users to specify how many pages to scrape and a maximum price
    # Re-initialize the scraper with the specified number of pages
    if pages < 1 or pages > 50:  # Basic validation for page number
        raise HTTPException(status_code=400, detail="Pages must be between 1 and 50.")
    my_scraper = BookScraper(base_url="http://books.toscrape.com/", total_pages=pages)
    my_scraper.run()  # Run the scraping process
    
    # Convert scraped books to a list of dictionaries
    scraped_data = [book.to_dict() for book in my_scraper.scraped_books]
    
    if max_price is not None:
        # Filter books by price if max_price is provided
        scraped_data = [book for book in scraped_data if book['Price'] <= max_price]
    # FastAPI automatically converts this dictionary into clean JSON for the web!
    return {"books": scraped_data}

# 4. Add book endpoint
@app.post("/add-book")
def add_book(book: NewBook):
    # 1. Convert the validated Pydantic object into a dictionary
    book_dict = book.model_dump() 
    
    # 2. Add it to our mock database
    custom_books_db.append(book_dict)
    
    # 3. Return a success message and the data
    return {"message": "Book added successfully!", "book": book_dict}

# (Optional) You can leave this completely empty now, or use it for testing 
# if you ever run the file directly with 'python book_api.py'
if __name__ == "__main__":
    pass