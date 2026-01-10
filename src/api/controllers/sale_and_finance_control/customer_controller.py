# src/api/controllers/sale_and_finance_control/customer_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/', methods=['POST'])
@token_required
@inject
def add_new_customer(customer_service = Provide[Container.customer_service]): # Phải khai báo ở đây
    try:
        data = request.get_json()
        # Tự gán owner_id từ token để bảo mật
        data['owner_id'] = getattr(request, 'current_user_id', None)
        result = customer_service.create_customer(data)
        return jsonify({"message": "Thành công", "id": result.customer_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@customer_bp.route('/', methods=['GET'])
@token_required
@inject
def get_all_customers(customer_service = Provide[Container.customer_service]): # Phải khai báo ở đây
    try:
        owner_id = getattr(request, 'current_user_id', None)
        # Lấy danh sách khách hàng của shop đó
        customers = customer_service.repository.get_all_by_owner(owner_id)
        return jsonify([{
            "id": c.customer_id, 
            "name": c.customer_name, 
            "phone": c.phone_number,
            "address": c.address
        } for c in customers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customer_bp.route('/<int:id>', methods=['PUT'])
@token_required
@inject
def update_customer(id, customer_service = Provide[Container.customer_service]):
    try:
        data = request.get_json()
        customer_service.update_customer(id, data)
        return jsonify({"message": "Cập nhật thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@customer_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@inject
def delete_customer(id, customer_service = Provide[Container.customer_service]):
    try:
        customer_service.delete_customer(id)
        return jsonify({"message": "Xóa thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400