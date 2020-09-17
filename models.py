from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#########SETUP#########
db_user = "xxx"
db_password = "xxx"
db_name = "xxx"
db_host = "xxx"
db_port = "xxx"

app = Flask(__name__)

app.config["SECRET_KEY"] = "secretkey"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


#########MODELS########
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.Text)
    name = db.Column(db.Text)
    surname = db.Column(db.Text)
    email = db.Column(db.Text)
    notes = db.relationship(
        "Note", backref="user", cascade="all, delete, delete-orphan", lazy=True
    )

    def __init__(self, nick, name, surname, email):
        self.nick = nick
        self.name = name
        self.surname = surname
        self.email = email

    def __repr__(self):
        return (
            f"<User id: %s nick: %s name: %s surname: %s email: %s>"
            % self.id
            % self.nick
            % self.name
            % self.surname
            % self.email
        )

    def get_notes(self):
        print(f"Notes by {user.name}")
        for note in self.notes:
            print(note.note)


class Note(db.Model):
    __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text)
    time = db.Column(db.Text)
    location = db.Column(db.Text)
    street = db.Column(db.Text)
    city = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, note, time, location, street, city, user_id):
        self.note = note
        self.time = time
        self.location = location
        self.street = street
        self.city = city
        self.user_id = user_id

    def __repr__(self):
        return (
            f"<Note id: %s note: %s time: %s location: %s street: %s city: %s user_id: %s>"
            % self.id
            % self.note
            % self.time
            % self.location
            % self.street
            % self.city
            % self.user_id
        )