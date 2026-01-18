from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.auth_service import AuthService
import json

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
@inject
def login(auth_service: AuthService = Provide[Container.auth_service]):
    try:
        data = request.json
        if not data:
             return jsonify({'message': 'Missing JSON body'}), 400
             
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400

        result = auth_service.login(email, password)
        if result:
            return jsonify(result), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/refresh-token', methods=['POST'])
@inject
def refresh_token(auth_service: AuthService = Provide[Container.auth_service]):
    try:
        data = request.json
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({'message': 'Refresh token is required'}), 400
            
        result = auth_service.refresh_token(refresh_token)
        if result:
            return jsonify(result), 200
        return jsonify({'message': 'Invalid refresh token'}), 401
    except Exception as e:
         return jsonify({'message': str(e)}), 500