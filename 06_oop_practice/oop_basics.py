# 1. We define the Blueprint (Class) using the 'class' keyword.
# Convention is to use Capitalized words for Classes.
class Movie:    
    # 2. The __init__ function (The Constructor)
    # This runs the exact moment we create a new movie. 
    # 'self' refers to the specific object being created.
    def __init__(self, title, year, duration_mins):
        self.title = title
        self.year = year
        self.duration_mins = duration_mins
        self.is_played = False  # Default state
        
    # 3. We define Behaviors (Methods)
    # Notice how we don't need to pass the title or year in! 
    # It already knows them because of 'self'.
    def play(self):
        print(f"▶️ Now playing: {self.title} ({self.year})")
        self.is_played = True
        
    def get_status(self):
        status = "Watched" if self.is_played else "Unwatched"
        print(f"🎬 {self.title} is currently: {status}")

# 4. We can create another class to manage our collection of movies.
class MediaLibrary:
    def __init__(self):
        self.movies = []
    
    def add_movie(self, movie: Movie):
        # This actively stops bad data from crashing your app later.
        if not isinstance(movie, Movie):
            print("❌ Error: You can only add Movie objects to the library!")
            return  # Stop the function

        self.movies.append(movie)
        print(f"Added '{movie.title}' to the library.")
    
    def show_unwatched(self):
        print("🎥 Unwatched Movies in Library:")
        for movie in self.movies:
            if not movie.is_played:
                print(f"- {movie.title} ({movie.year})")

# --- Let's use our Blueprint! ---
if __name__ == "__main__":
    myMediaLibrary = MediaLibrary()
    # We create two distinct "Instances" (Objects) from the Movie class
    movie1 = Movie("The Matrix", 1999, 136)
    movie2 = Movie("Dune: Part Two", 2024, 166)
    
    myMediaLibrary.add_movie(movie1)
    myMediaLibrary.add_movie(movie2)
    myMediaLibrary.add_movie(123)  # This will trigger our error handling!
    # They both share the same behaviors, but hold different data
    movie1.get_status()
    movie2.get_status()
    
    print("-" * 20)
    
    # Let's watch The Matrix
    movie1.play()
    
    print("-" * 20)
    
    # Check status again
    movie1.get_status()
    movie2.get_status()

    print("-" * 20)
    # Show unwatched movies in the library
    myMediaLibrary.show_unwatched()