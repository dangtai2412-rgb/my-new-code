from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from api.schemas.order import OrderSchema
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

order_bp = Blueprint('order_bp', __name__)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@order_bp.route('/', methods=['POST'])
@token_required
@inject
def create_order(current_user, service=Provide[Container.order_service]):
    """
    Tạo đơn hàng mới (Bán hàng)
    ---
    tags:
      - Sale & Finance - Orders
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        description: Thông tin đơn hàng cần tạo
        required: true
        schema:
          type: object
          required:
            - customer_id
            - details
          properties:
            customer_id:
              type: integer
              example: 1
              description: ID Khách hàng mua
            details:
              type: array
              description: Danh sách sản phẩm
              items:
                type: object
                properties:
                  product_id:
                    type: integer
                    example: 2
                  quantity:
                    type: integer
                    example: 10
                  unit_price:
                    type: number
                    example: 50000
                    description: (Tùy chọn) Nếu không nhập sẽ lấy giá mặc định
    responses:
      201:
        description: Tạo đơn hàng thành công
      400:
        description: Dữ liệu đầu vào không hợp lệ
      500:
        description: Lỗi Server
    """
    data = request.get_json()
    try:
        # Validate data
        errors = order_schema.validate(data)
        if errors:
            return jsonify(errors), 400
            
        new_order = service.create_order(data, current_user.owner_id)
        return jsonify(order_schema.dump(new_order)), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@order_bp.route('/', methods=['GET'])
@token_required
@inject
def get_orders(current_user, service=Provide[Container.order_service]):
    """
    Lấy danh sách đơn hàng
    ---
    tags:
      - Sale & Finance - Orders
    security:
      - Bearer: []
    responses:
      200:
        description: Danh sách đơn hàng
    """
    orders = service.get_orders(current_user.owner_id)
    return jsonify(orders_schema.dump(orders)), 200

@order_bp.route('/<int:order_id>', methods=['GET'])
@token_required
@inject
def get_order_detail(order_id, current_user, service=Provide[Container.order_service]):
    """
    Xem chi tiết một đơn hàng
    ---
    tags:
      - Sale & Finance - Orders
    security:
      - Bearer: []
    parameters:
      - in: path
        name: order_id
        type: integer
        required: true
        description: ID đơn hàng
    responses:
      200:
        description: Thông tin chi tiết đơn hàng
      404:
        description: Không tìm thấy đơn hàng
    """
    order = service.get_order_by_id(order_id)
    if not order or order.owner_id != current_user.owner_id:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order_schema.dump(order)), 200