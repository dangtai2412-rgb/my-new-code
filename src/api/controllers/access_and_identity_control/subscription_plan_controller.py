from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

subscription_plan_bp = Blueprint('subscription_plan_bp', __name__)

@subscription_plan_bp.route('/', methods=['POST'])
@token_required
@inject
def create_new_subscription_plan(plan_service = Provide[Container.subscription_plan_service]):
    """
    Tạo gói cước dịch vụ mới (Admin Only)
    ---
    tags:
      - Subscription Plan
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - plan_name
            - price
          properties:
            plan_name:
              type: string
              example: "Gói Cơ Bản (Basic)"
            price:
              type: number
              format: float
              example: 199000
            duration_months:
              type: integer
              example: 6
              description: Thời hạn gói (tháng)
            description:
              type: string
              example: "Dành cho cửa hàng nhỏ, tối đa 2 nhân viên"
    responses:
      201:
        description: Tạo gói cước thành công
    """
    try:
        data = request.get_json()
        result = plan_service.create_plan(data)
        return jsonify({"message": "Tạo gói cước thành công", "id": result.plan_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@subscription_plan_bp.route('/', methods=['GET'])
@inject
def list_all_plans(plan_service = Provide[Container.subscription_plan_service]):
    """
    Lấy danh sách các gói cước (Public)
    ---
    tags:
      - Subscription Plan
    responses:
      200:
        description: Danh sách gói cước
    """
    try:
        plans = plan_service.get_all_plans()
        return jsonify([
            {"id": p.plan_id, "name": p.plan_name, "price": float(p.price)} 
            for p in plans
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500