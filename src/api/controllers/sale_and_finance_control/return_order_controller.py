from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from api.schemas.return_order import ReturnOrderSchema
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

return_order_bp = Blueprint('return_order_bp', __name__)
return_schema = ReturnOrderSchema()
returns_schema = ReturnOrderSchema(many=True)

@return_order_bp.route('/', methods=['POST'])
@token_required
@inject
def create_return_order(current_user, service=Provide[Container.return_order_service]):
    """
    Tạo phiếu trả hàng
    ---
    tags:
      - Sale & Finance - Return
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - customer_id
            - details
          properties:
            customer_id:
              type: integer
            reason:
              type: string
              example: "Dư dùng"
            details:
              type: array
              items:
                type: object
                properties:
                  product_id:
                    type: integer
                  quantity:
                    type: integer
                  refund_price:
                    type: number
    """
    data = request.get_json()
    new_ro = service.create_return(data, current_user.owner_id)
    return jsonify(return_schema.dump(new_ro)), 201

@return_order_bp.route('/', methods=['GET'])
@token_required
@inject
def get_return_history(current_user, service=Provide[Container.return_order_service]):
    """Lấy lịch sử trả hàng"""
    history = service.get_history(current_user.owner_id)
    return jsonify(returns_schema.dump(history)), 200