from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

## Routes

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_list)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return make_response(jsonify({'error': 'Hero not found'}), 404)

    powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]

    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    }

    return jsonify(hero_data)

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_list)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return make_response(jsonify({'error': 'Power not found'}), 404)

    power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description
    }

    return jsonify(power_data)

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return make_response(jsonify({'error': 'Power not found'}), 404)

    data = request.get_json()
    if 'description' not in data:
        return make_response(jsonify({'error': 'Description is required'}), 400)

    description = data['description']
    power.description = description

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)

    power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description
    }

    return jsonify(power_data)



if __name__ == '__main__':
    app.run(port=5555)


