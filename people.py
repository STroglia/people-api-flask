from flask import abort, make_response, request
from config import db
from models import Person, people_schema, person_schema

def read_all():
    people = Person.query.order_by(Person.lname).all()
    return people_schema.dump(people)

def read_one(lname):
    person = Person.query.filter(Person.lname.ilike(lname)).one_or_none()
    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"Persona con apellido {lname} no encontrada")

def create():
    person_data = request.get_json()
    lname = person_data.get("lname")
    existing_person = Person.query.filter(Person.lname.ilike(lname)).one_or_none()
    
    if existing_person is None:
        new_person = Person(fname=person_data.get("fname"), lname=lname)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person), 201
    else:
        abort(409, f"La persona con apellido {lname} ya existe")

def update(lname):
    update_person = Person.query.filter(Person.lname.ilike(lname)).one_or_none()
    
    if update_person is not None:
        person_data = request.get_json()
        
        # Actualizamos solo si vienen los campos en el JSON y evitamos duplicados
        new_lname = person_data.get("lname", update_person.lname)
        if new_lname.lower() != update_person.lname.lower():
            existing = Person.query.filter(Person.lname.ilike(new_lname)).one_or_none()
            if existing is not None:
                abort(409, f"El apellido {new_lname} ya pertenece a otra persona")
        
        update_person.fname = person_data.get("fname", update_person.fname)
        update_person.lname = new_lname
        
        db.session.commit()
        return person_schema.dump(update_person), 200
    else:
        abort(404, f"Persona con apellido {lname} no encontrada")

def delete(lname):
    person = Person.query.filter(Person.lname.ilike(lname)).one_or_none()
    
    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return make_response(f"Persona con apellido {lname} eliminada", 200)
    else:
        abort(404, f"Persona con apellido {lname} no encontrada")