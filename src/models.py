from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    #relationship
    favorite: Mapped["Favorite"] = relationship(back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[str] = mapped_column(String(120))
    mass: Mapped[str] = mapped_column(String(120))
    hair_color: Mapped[str] = mapped_column(String(120))

    # relationships
    favorites: Mapped[List["Favorite"]] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    diameter: Mapped[str] = mapped_column(String(120))
    climate: Mapped[str] = mapped_column(String(120))
    terrain: Mapped[str] = mapped_column(String(120))

    #relationships
    favorites: Mapped[List["Favorite"]] = relationship()

    def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
            }

class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    #relationships
    #one to one with class User
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorite")

    # one to many with class Chracter and Planet
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))

    
