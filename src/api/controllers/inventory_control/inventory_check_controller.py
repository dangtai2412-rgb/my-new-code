from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from api.schemas.inventory_check import InventoryCheckSchema
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

inventory_check_bp = Blueprint('inventory_check_bp', __name__)
check_schema = InventoryCheckSchema()

@inventory_check_bp.route('/', methods=['POST'])
@token_required
@inject
def create_inventory_check(current_user, service=Provide[Container.inventory_check_service]):
    """
    Tạo phiếu kiểm kho (Cân bằng kho)
    ---
    tags:
      - Inventory - Checks
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            note:
              type: string
              example: "Kiểm kho cuối tháng 1"
            details:
              type: array
              items:
                type: object
                properties:
                  product_id:
                    type: integer
                    example: 1
                  actual_quantity:
                    type: integer
                    example: 98
    """
    data = request.get_json()
    try:
        new_check = service.create_check(data, current_user.owner_id)
        return jsonify({"message": "Đã cân bằng kho thành công!", "code": new_check.check_code}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@inventory_check_bp.route('/', methods=['GET'])
@token_required
@inject
def get_history(current_user, service=Provide[Container.inventory_check_service]):
    """Lấy lịch sử kiểm kho"""
    history = service.get_history(current_user.owner_id)
    # Note: Cần viết schema dump list nếu muốn trả về đẹp, ở đây mình trả text demo
    return jsonify([{"code": h.check_code, "date": h.check_date, "note": h.note} for h in history]), 200