# URLSHORTNER

Steps before running the app:

### 1. Clone the project  

project structure:
  -urlshortner(root)
    - app
    - migrations
    - requirements.txt
    - main.py

### 2. Create and activate virtual environment on root directory terminal:

    python -m venv env
    env\Scripts\activate

### 3. Install required packages:  
    In  root terminal, after activating venv type:
        pip install -r requirements.txt

### 4. Create a .env file.  

The .env file should contain:

- DATABASE_HOSTNAME = 
- DATABASE_PORT = 
- DATABASE_PASSWORD = 
- DATABASE_NAME = 
- DATABASE_USERNAME =  

### 5. Edit the app/db.py with database of your choice

    f{"mysql+aiomysql://"} to the database driver of your choice. Rest remains unchanged

### 6. Run the app:

- cd into the root project folder
- on terminal type  
    ### **uvicorn: main:app**  

    (if for development purpose:)
    
    ### **uvicorn main:app --reload**
    
 
