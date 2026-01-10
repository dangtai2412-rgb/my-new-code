# src/api/controllers/inventory_control/stock_import_detail_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

stock_import_detail_bp = Blueprint('stock_import_detail_bp', __name__)

@stock_import_detail_bp.route('/', methods=['POST'])
@token_required
@inject
def add_detail(service = Provide[Container.stock_import_detail_service]):
    try:
        data = request.get_json()
        detail = service.create_detail(data)
        return jsonify({"id": detail.detail_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400