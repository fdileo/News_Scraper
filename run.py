from app import create_app, db
from app.models import Articles 
from flask import current_app

app = create_app()

if __name__ == "__main__":
    
    with app.app_context():
        
        db.create_all()
        print("Tabelle create con successo!")
        
    app.run(debug=True)