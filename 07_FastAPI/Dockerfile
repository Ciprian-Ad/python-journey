# 1. Base Image: Start with a lightweight version of Python
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the shopping list into the container
COPY requirements.txt .

# 4. Install the libraries (the --no-cache-dir keeps the container small!)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all your code files into the container
COPY . .

# 6. Expose the port Uvicorn will run on
EXPOSE 8000

# 7. The command to start the server when the container launches
# Notice we use "0.0.0.0" so it's accessible outside the container!
CMD ["uvicorn", "book_api:app", "--host", "0.0.0.0", "--port", "8000"]