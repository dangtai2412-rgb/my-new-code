# src/api/controllers/inventory_control/unit_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

unit_bp = Blueprint('unit_bp', __name__)

@unit_bp.route('/', methods=['POST'])
@token_required
@inject
def create_new_unit(unit_service = Provide[Container.unit_service]):
    """
    Tạo đơn vị tính (Thùng, Lon, Cái)
    ---
    tags: [Inventory]
    security: [{BearerAuth: []}]
    """
    try:
        data = request.get_json()
        result = unit_service.create_unit(data)
        return jsonify({"id": result.unit_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@unit_bp.route('/product/<int:product_id>', methods=['GET'])
@token_required
@inject
def list_units_by_product(product_id, unit_service = Provide[Container.unit_service]):
    try:
        units = unit_service.get_units_by_product(product_id)
        return jsonify([{"id": u.unit_id, "name": u.unit_name} for u in units]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@unit_bp.route('/<int:unit_id>', methods=['DELETE'])
@token_required
@inject
def delete_unit(unit_id, unit_service = Provide[Container.unit_service]):
    try:
        unit_service.delete_unit(unit_id)
        return jsonify({"message": "Deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400