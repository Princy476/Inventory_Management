from app.routes import app
from app.database import initialize_db

if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)
