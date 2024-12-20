from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import db, User, Car, Service, Appointment, Invoice, Log
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'])
        new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password, role_id=data['role_id'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@api.route('/cars', methods=['GET'])
@jwt_required()
def get_cars():
    user_id = get_jwt_identity()
    cars = Car.query.filter_by(user_id=user_id).all()
    return jsonify([car.serialize() for car in cars]), 200

@api.route('/cars', methods=['POST'])
@jwt_required()
def add_car():
    data = request.get_json()
    new_car = Car(
        user_id=get_jwt_identity(),
        make=data['make'],
        model=data['model'],
        year=data['year'],
        vin=data['vin'],
        license_plate=data['license_plate']
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({"message": "Car added successfully"}), 201

@api.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([service.serialize() for service in services]), 200

@api.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    new_appointment = Appointment(car_id=data['car_id'], service_id=data['service_id'], date=data['date'], time=data['time'], status=data['status'])
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({"message": "Appointment created successfully"}), 201

@api.route('/invoices', methods=['GET'])
@jwt_required()
def get_invoices():
    user_id = get_jwt_identity()
    invoices = Invoice.query.join(Appointment).join(Car).filter(Car.user_id == user_id).all()
    return jsonify([invoice.serialize() for invoice in invoices]), 200

@api.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    user_id = get_jwt_identity()
    logs = Log.query.filter_by(user_id=user_id).all()
    return jsonify([log.serialize() for log in logs]), 200

