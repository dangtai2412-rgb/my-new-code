from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required # Dùng ổ khóa
from infrastructure.repositories.sale_and_finance_repo.order_repository import OrderRepository
from services.sale_and_finance_service.order_service import OrderService
from infrastructure.databases.mssql import session
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

order_bp = Blueprint('order_bp', __name__)



@order_bp.route('/', methods=['POST'])
@token_required # BẮT BUỘC PHẢI CÓ TOKEN MỚI ĐƯỢC MUA HÀNG
@inject
def post_order(): # Đổi tên hàm để tránh lỗi AssertionError
    """
    Tạo đơn hàng
    ---
    tags: [Orders]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            customer_id: {type: integer, example: 1}
            employee_id: {type: integer, example: 1}
            items:
              type: array
              items:
                type: object
                properties:
                  product_id: {type: integer, example: 1}
                  unit_id: {type: integer, example: 1}
                  quantity: {type: integer, example: 2}
                  unit_price: {type: number, example: 50000}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        result = service.create_order(data)
        return jsonify({
            "message": "Tạo đơn thành công", 
            "order_id": result.order_id,
            "total_amount": float(result.total_amount)
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400