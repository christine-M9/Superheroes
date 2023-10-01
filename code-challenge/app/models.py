from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)

    powers = db.relationship('Power', secondary='hero_power', back_populates='heroes')

class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    heroes = db.relationship('Hero', secondary='hero_power', back_populates='powers')

class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    strength = db.Column(db.String(255), nullable=False)

    hero = db.relationship('Hero', backref=db.backref('hero_powers', cascade='all, delete-orphan'))
    power = db.relationship('Power', backref=db.backref('hero_powers', cascade='all, delete-orphan'))


