from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

debt_bp = Blueprint('debt_bp', __name__)

@debt_bp.route('/', methods=['POST'])
@token_required
@inject
def create_customer_debt(debt_service = Provide[Container.debt_service]):
    """
    Ghi nhận công nợ mới
    ---
    tags: [Finance & Debt]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            order_id: {type: integer, example: 1}
            customer_id: {type: integer, example: 1}
            debt_amount: {type: number, example: 500000}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        # Gọi service thay vì gọi trực tiếp
        result = debt_service.create_debt_from_order(
            data.get('order_id'), 
            data.get('customer_id'), 
            data.get('debt_amount')
        )
        return jsonify({"message": "Ghi nợ thành công", "id": result.debt_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400