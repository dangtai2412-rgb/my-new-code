# src/api/controllers/inventory_control/stock_import_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

stock_import_bp = Blueprint('stock_import_bp', __name__)

@stock_import_bp.route('/', methods=['POST'])
@token_required
@inject
def import_goods(stock_service = Provide[Container.stock_import_service]):
    """
    Tạo phiếu nhập hàng
    ---
    tags: [Inventory Control]
    security: [{BearerAuth: []}]
    """
    try:
        data = request.get_json()
        owner_id = getattr(request, 'current_user_id', None)
        result = stock_service.create_stock_import(data, owner_id)
        return jsonify({"message": "Success", "import_id": result.import_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@stock_import_bp.route('/', methods=['GET'])
@token_required
@inject
def get_import_history(stock_service = Provide[Container.stock_import_service]):
    """Lấy danh sách lịch sử nhập hàng"""
    owner_id = getattr(request, 'current_user_id', None)
    history = stock_service.get_history_by_owner(owner_id)
    return jsonify(history), 200