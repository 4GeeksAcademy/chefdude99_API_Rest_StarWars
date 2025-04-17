from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    characters_favorites: Mapped[list['Fav_character']] = relationship(back_populates='user', cascade='all, delete-orphan')
    starships_favorites: Mapped[list['Fav_starship']] = relationship(back_populates='user', cascade='all, delete-orphan')
    planets_favorites: Mapped[list['Fav_planet']] = relationship(back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return self.name
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname,
            'email': self.email,
            'character_favorites': [fav.character_id for fav in self.characters_favorites],
            'starships_favorites': [fav.starship_id for fav in self.starships_favorites],
            'planets_favorites': [fav.planet_id for fav in self.planets_favorites]
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    heigth: Mapped[int] = mapped_column(Integer, nullable=False)
    favorites: Mapped[list['Fav_character']] = relationship('Fav_character', back_populates='character', cascade='all, delete-orphan')

    def __repr__(self):
        return self.name
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'heigth': self.heigth,
            'favorites': [fav.user.name for fav in self.favorites]
        }

class Starships(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    size: Mapped[str] = mapped_column(String(1000), nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    favorites: Mapped[list['Fav_starship']] = relationship('Fav_starship', back_populates='starship', cascade='all, delete-orphan')

    def __repr__(self):
        return self.name
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'size': self.size,
            'seats': self.size,
            'favorites': [fav.user.name for fav in self.favorites]
        }


class Planets(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    favorites: Mapped[list['Fav_planet']] = relationship('Fav_planet', back_populates='planet', cascade='all, delete-orphan')

    def __repr__(self):
        return self.name
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'favorites': [fav.user.name for fav in self.favorites]
        }


class Fav_character(db.Model):
    __tablename__ = 'fav_character'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))
    user: Mapped['User'] = relationship('User', foreign_keys=[user_id], back_populates='characters_favorites')
    character: Mapped['Characters'] = relationship('Characters', foreign_keys=[character_id], back_populates='favorites')

    def __repr__(self):
        return f'A {self.user.name} Le gusta {self.character.name}'
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'character_id': self.character_id,
            'user': self.user.name,
            'character': self.character.name
        }
    
class Fav_starship(db.Model):
    __tablename__ = 'fav_starship'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    starship_id: Mapped[int] = mapped_column(ForeignKey('starships.id'))
    user: Mapped['User'] = relationship(back_populates='starships_favorites')
    starship: Mapped['Starships'] = relationship(back_populates='favorites')

    def __repr__(self):
        return f'A {self.user.name} Le gusta {self.starship.name}'
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'starship_id': self.starship_id,
            'user': self.user.name,
            'starship': self.starship.name
        }

class Fav_planet(db.Model):
    __tablename__ = 'fav_planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    user: Mapped['User'] = relationship(back_populates='planets_favorites')
    planet: Mapped['Planets'] = relationship(back_populates='favorites')

    def __repr__(self):
        return f'A {self.user.name} Le gusta {self.planet.name}'
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.planet_id,
            'user': self.user.name,
            'planet': self.planet.name
        }







    


   