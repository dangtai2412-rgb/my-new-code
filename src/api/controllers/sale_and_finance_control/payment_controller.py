from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/', methods=['POST'])
@token_required
@inject
def process_debt_payment(payment_service = Provide[Container.payment_service]):
    """
    Thanh toán công nợ
    ---
    tags: [Finance & Debt]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            debt_id: {type: integer, example: 1}
            amount: {type: number, example: 200000}
            payment_method: {type: string, example: "Transfer"}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        result = payment_service.process_payment(
            data.get('debt_id'), 
            data.get('amount'), 
            data.get('payment_method')
        )
        return jsonify({"message": "Thanh toán thành công", "payment_id": result.payment_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400