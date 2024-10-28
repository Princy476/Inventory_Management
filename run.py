from app.routes import app
from app.database import initialize_db

if __name__ == '__main__':
    # Initialize the database
    initialize_db()
    
    # Run the Flask app
    app.run(debug=True)
