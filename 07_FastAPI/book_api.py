from oop_book_scraper import BookScraper, Book
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# --- 1. Database Setup ---
# We tell SQLAlchemy to create a local SQLite file called 'books.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/books.db"

# The Engine is the core connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# The Session is what we use to actually talk to the database (add, delete, commit)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The Base is the parent class for all our database models
Base = declarative_base()

# --- 2. The Database Model (SQLAlchemy) ---
class DBBook(Base):
    __tablename__ = "books"  # The actual name of the table in SQLite

    # Define the columns
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)

# --- 3. Create the Database ---
# This line tells SQLAlchemy to look at all classes that inherit from 'Base' 
# and automatically create the tables in the SQLite file!
Base.metadata.create_all(bind=engine)

# --- 4. Database Dependency ---
# This is a FastAPI trick. It opens a database session when a request comes in, 
# and safely closes it when the request is done.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class NewBook(BaseModel):
    title: str
    price: float
# 1. Initialize the app globally so Uvicorn can find it
app = FastAPI()
#storage for custom books added via the API (not scraped)


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
def add_book(book: NewBook, db: Session = Depends(get_db)):
    # 1. Map the Pydantic object to the SQLAlchemy model
    new_db_book = DBBook(title=book.title, price=book.price)
    
    # 2. Stage the object to be saved
    db.add(new_db_book)
    
    # 3. Commit the transaction (Write it to books.db!)
    db.commit()
    
    # 4. Refresh the object to get its new database ID
    db.refresh(new_db_book)
    
    return {"message": "Book saved permanently!", "book": new_db_book}

# 5. Get all books endpoint
@app.get("/books")
def get_saved_books(db: Session = Depends(get_db)):
    # Query all books from the database
    all_books = db.query(DBBook).all()
    
    # Convert SQLAlchemy objects to dictionaries for JSON response
    return {"books": [{"id": book.id, "title": book.title, "price": book.price} for book in all_books]}

# 6. Delete book endpoint
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    # Find the book by ID
    book_to_delete = db.query(DBBook).filter(DBBook.id == book_id).first()
    
    if not book_to_delete:
        raise HTTPException(status_code=404, detail="Book not found.")
    
    # Delete the book and commit the transaction
    db.delete(book_to_delete)
    db.commit()
    
    return {"message": f"Book {book_id} deleted successfully."}

# 7. Update book endpoint
@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: NewBook, db: Session = Depends(get_db)):
    # Find the book by ID
    book_to_update = db.query(DBBook).filter(DBBook.id == book_id).first()
    
    if not book_to_update:
        raise HTTPException(status_code=404, detail="Book not found.")
    
    # Update the book's attributes
    book_to_update.title = updated_book.title
    book_to_update.price = updated_book.price
    
    # Commit the transaction to save changes
    db.commit()
    db.refresh(book_to_update)
    
    return {"message": f"Book {book_id} updated successfully.", "book": {"id": book_id, "title": updated_book.title, "price": updated_book.price}}
# (Optional) You can leave this completely empty now, or use it for testing 
# if you ever run the file directly with 'python book_api.py'
if __name__ == "__main__":
    pass