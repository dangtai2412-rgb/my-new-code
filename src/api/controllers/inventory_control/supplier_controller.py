# src/api/controllers/inventory_control/supplier_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

supplier_bp = Blueprint('supplier_bp', __name__)

@supplier_bp.route('/', methods=['POST'])
@token_required
@inject
def add_supplier(supplier_service = Provide[Container.supplier_service]):
    """
    Thêm nhà cung cấp
    ---
    tags: [Suppliers]
    security: [{BearerAuth: []}]
    """
    try:
        data = request.get_json()
        owner_id = getattr(request, 'current_user_id', None)
        supplier = supplier_service.create_supplier(data, owner_id)
        return jsonify({"id": supplier.supplier_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@supplier_bp.route('/', methods=['GET'])
@token_required
@inject
def get_suppliers(supplier_service = Provide[Container.supplier_service]):
    """
    Lấy danh sách nhà cung cấp
    ---
    tags: [Suppliers]
    security: [{BearerAuth: []}]
    """
    owner_id = getattr(request, 'current_user_id', None)
    suppliers = supplier_service.get_suppliers_by_owner(owner_id)
    return jsonify([{"id": s.supplier_id, "name": s.supplier_name} for s in suppliers]), 200
@supplier_bp.route('/<int:supplier_id>', methods=['PUT'])
@token_required
@inject
def update_supplier(supplier_id, supplier_service = Provide[Container.supplier_service]):
    try:
        data = request.get_json()
        supplier_service.update_supplier(supplier_id, data)
        return jsonify({"message": "Success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400