from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(20), nullable=False)
    Lastname: Mapped[str] = mapped_column(String(20), nullable=False)
    Email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

class Characters(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(20), nullable=False)
    Heigth: Mapped[int] = mapped_column(Integer, nullable=False)

class Starships(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(20), nullable=False)
    Size: Mapped[str] = mapped_column(String(1000), nullable=False)
    Seats: Mapped[int] = mapped_column(Integer, nullable=False)

class Planets(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(20), nullable=False)
    Number: Mapped[int] = mapped_column(Integer, nullable=False)


class Fav_character(db.Model):
    __tablename__ = 'fav_character'
    id: Mapped[int] = mapped_column(primary_key=True)
    User: Mapped[str] = mapped_column(ForeignKey('user.id'))
    Character: Mapped[str] = mapped_column(ForeignKey('characters.id'))


class Fav_starship(db.Model):
    __tablename__ = 'fav_starship'
    id: Mapped[int] = mapped_column(primary_key=True)
    User: Mapped[str] = mapped_column(ForeignKey('user.id'))
    Starship: Mapped[str] = mapped_column(ForeignKey('starships.id'))


class Fav_planet(db.Model):
    __tablename__ = 'fav_planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    User: Mapped[str] = mapped_column(ForeignKey('user.id'))
    Planet: Mapped[str] = mapped_column(ForeignKey('planets.id'))



    


   