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
    Tạo gói cước dịch vụ mới
    """
    try:
        data = request.get_json()
        result = plan_service.create_plan(data)
        return jsonify({"message": "Tạo gói cước thành công", "id": result.plan_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@subscription_plan_bp.route('/', methods=['GET'])
@inject  # Có thể không cần token nếu muốn public danh sách gói cước
def list_all_plans(plan_service = Provide[Container.subscription_plan_service]):
    """
    Lấy danh sách các gói cước
    """
    try:
        plans = plan_service.get_all_plans()
        return jsonify([
            {"id": p.plan_id, "name": p.plan_name, "price": float(p.price)} 
            for p in plans
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500