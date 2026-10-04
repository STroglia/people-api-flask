import os
from config import db, app
from models import Person

PEOPLE = [
    {"fname": "Doug", "lname": "Farrell"},
    {"fname": "Kent", "lname": "Brockman"},
    {"fname": "Ezra", "lname": "Miller"},
]

if os.path.exists("people.db"):
    os.remove("people.db")

with app.app_context():
    db.create_all()
    
    for data in PEOPLE:
        new_person = Person(fname=data["fname"], lname=data["lname"])
        db.session.add(new_person)
        
    db.session.commit()
    print("Base de datos creada exitosamente.")