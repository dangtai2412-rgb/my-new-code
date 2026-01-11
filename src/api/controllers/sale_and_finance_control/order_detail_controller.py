from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

order_detail_bp = Blueprint('order_detail_bp', __name__)

@order_detail_bp.route('/', methods=['POST'])
@token_required
@inject
def add_order_detail(detail_service = Provide[Container.order_detail_service]):
    """
    Thêm chi tiết sản phẩm vào đơn hàng
    ---
    tags: [Order Details]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            order_id: {type: integer, example: 1}
            product_id: {type: integer, example: 1}
            quantity: {type: integer, example: 10}
            unit_price: {type: number, example: 50000}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        # Service sẽ lo việc tạo model và tính toán line_total
        result = detail_service.create_detail(data)
        return jsonify({"message": "Thêm chi tiết thành công", "id": result.detail_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500