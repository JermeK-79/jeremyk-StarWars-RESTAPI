from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Text
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
    
    # Relationships
    favorites: Mapped[List["Favorite"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan",
        lazy='select'
    )
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class Character(db.Model):
    __tablename__ = 'character'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    mass: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    hair_color: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    skin_color: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    eye_color: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    favorites: Mapped[List["Favorite"]] = relationship(
        back_populates="character",
        lazy='select'
    )
    
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
    
    def __repr__(self):
        return f'<Character {self.name}>'


class Planet(db.Model):
    __tablename__ = 'planet'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    diameter: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    rotation_period: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    orbital_period: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    gravity: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    population: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    climate: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    terrain: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    favorites: Mapped[List["Favorite"]] = relationship(
        back_populates="planet",
        lazy='select'
    )
    
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
    
    def __repr__(self):
        return f'<Planet {self.name}>'


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(String(120), nullable=False)
    vehicle_class: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    manufacturer: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    cost_in_credits: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    length: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    crew: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    passengers: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    
    # Relationships
    favorites: Mapped[List["Favorite"]] = relationship(
        back_populates="vehicle",
        lazy='select'
    )
    
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
    
    def __repr__(self):
        return f'<Vehicle {self.model}>'


class Favorite(db.Model):
    __tablename__ = 'favorite'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Foreign Keys
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    character_id: Mapped[Optional[int]] = mapped_column(ForeignKey("character.id", ondelete="CASCADE"), nullable=True)
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id", ondelete="CASCADE"), nullable=True)
    vehicle_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vehicle.id", ondelete="CASCADE"), nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="favorites")
    character: Mapped[Optional["Character"]] = relationship(back_populates="favorites")
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="favorites")
    vehicle: Mapped[Optional["Vehicle"]] = relationship(back_populates="favorites")
    
    def serialize(self):
        result = {
            "id": self.id,
            "user_id": self.user_id,
        }
        
        if self.character_id:
            result["character_id"] = self.character_id
            result["character_name"] = self.character.name if self.character else None
        
        if self.planet_id:
            result["planet_id"] = self.planet_id
            result["planet_name"] = self.planet.name if self.planet else None
        
        if self.vehicle_id:
            result["vehicle_id"] = self.vehicle_id
            result["vehicle_model"] = self.vehicle.model if self.vehicle else None
        
        return result
    
    def __repr__(self):
        fav_type = "Character" if self.character_id else "Planet" if self.planet_id else "Vehicle"
        return f'<Favorite user={self.user_id} type={fav_type}>'