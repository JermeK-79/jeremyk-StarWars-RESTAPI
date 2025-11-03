from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = 'character'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[Optional[str]] = mapped_column(String(120))
    mass: Mapped[Optional[str]] = mapped_column(String(120))
    hair_color: Mapped[Optional[str]] = mapped_column(String(120))
    skin_color: Mapped[Optional[str]] = mapped_column(String(120))
    eye_color: Mapped[Optional[str]] = mapped_column(String(120))
    gender: Mapped[Optional[str]] = mapped_column(String(120))
    description: Mapped[Optional[str]] = mapped_column(String(500))
 
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="character")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "description": self.description
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    diameter: Mapped[Optional[str]] = mapped_column(String(120))
    rotation_period: Mapped[Optional[str]] = mapped_column(String(120))
    orbital_period: Mapped[Optional[str]] = mapped_column(String(120))
    gravity: Mapped[Optional[str]] = mapped_column(String(120))
    population: Mapped[Optional[str]] = mapped_column(String(120))
    climate: Mapped[Optional[str]] = mapped_column(String(120))
    terrain: Mapped[Optional[str]] = mapped_column(String(120))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Relationships
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="planet")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "description": self.description
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(String(120), nullable=False)
    vehicle_class: Mapped[Optional[str]] = mapped_column(String(120))
    manufacturer: Mapped[Optional[str]] = mapped_column(String(120))
    cost_in_credits: Mapped[Optional[str]] = mapped_column(String(120))
    length: Mapped[Optional[str]] = mapped_column(String(120))
    crew: Mapped[Optional[str]] = mapped_column(String(120))
    passengers: Mapped[Optional[str]] = mapped_column(String(120))
  
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="vehicle")
    
    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[Optional[int]] = mapped_column(ForeignKey("character.id"), nullable=True)
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"), nullable=True)
    vehicle_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vehicle.id"), nullable=True)
 
    user: Mapped["User"] = relationship(back_populates="favorites")
    character: Mapped[Optional["Character"]] = relationship(back_populates="favorites")
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="favorites")
    vehicle: Mapped[Optional["Vehicle"]] = relationship(back_populates="favorites")
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "character_name": self.character.name if self.character else None,
            "planet_id": self.planet_id,
            "planet_name": self.planet.name if self.planet else None,
            "vehicle_id": self.vehicle_id,
            "vehicle_model": self.vehicle.model if self.vehicle else None
        }