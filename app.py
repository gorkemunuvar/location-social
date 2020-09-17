import os
from flask import Flask, request
from models import app, db, User, Note


@app.route("/")
def index():
    return {"Welcome": "Home Page"}


@app.route("/users", methods=["GET", "POST"])
def user_api():
    if request.method == "GET":
        users = User.query.all()

        result = [
            {
                "id": user.id,
                "nick": user.nick,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
            }
            for user in users
        ]

        return {"count": len(result), "users": result}

    elif request.method == "POST":
        if request.is_json:
            json = request.get_json()

            new_user = User(
                json["nick"],
                json["name"],
                json["surname"],
                json["email"],
            )

            db.session.add(new_user)
            db.session.commit()

            return {"message": f"User {new_user.nick} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}


@app.route("/user/<user_id>", methods=["GET", "PUT", "DELETE"])
def handle_user(user_id):
    if request.method == "GET":
        user = User.query.filter_by(id=user_id).first()

        if user is not None:
            user_result = {
                "id": user.id,
                "nick": user.nick,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
            }

            return {"user": user_result}
        else:
            return {"Error": "No user with that id!"}

    elif request.method == "PUT":
        if request.is_json:
            user = User.query.filter_by(id=user_id).first()

            if user is not None:
                json = request.get_json()

                user.nick = json["nick"]
                user.name = json["name"]
                user.surname = json["surname"]
                user.email = json["email"]

                db.session.add(user)
                db.session.commit()

                return {"Message": f"User {user.nick} has been updated."}

            else:
                return {"Error": "No user with that id!"}

        else:
            return {"Message": "The request payload is not in JSON format"}

    elif request.method == "DELETE":
        user = User.query.filter_by(id=user_id).first()

        if user is not None:
            db.session.delete(user)
            db.session.commit()

            return {"Message": f"User {user.nick} has been deleted."}

        else:
            return {"Error": "No user with that id!"}


@app.route("/notes", methods=["GET", "POST"])
def note_api():
    if request.method == "GET":
        notes = Note.query.all()

        result = [
            {
                "id": note.id,
                "note": note.note,
                "time": note.time,
                "location": note.location,
                "street": note.street,
                "city": note.city,
                "user_id": note.user_id,
            }
            for note in notes
        ]

        return {"count": len(result), "notes": result}

    elif request.method == "POST":
        if request.is_json:
            json = request.get_json()

            new_note = Note(
                json["note"],
                json["time"],
                json["location"],
                json["street"],
                json["city"],
                json["user_id"],
            )

            db.session.add(new_note)
            db.session.commit()

            return {"message": f"User {new_note.note} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ["HOME"])
