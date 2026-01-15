from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

business_owner_bp = Blueprint('business_owner_bp', __name__)

@business_owner_bp.route('/', methods=['POST'])
@inject
def register_new_owner(owner_service = Provide[Container.business_owner_service]):
    """
    Đăng ký Chủ cửa hàng mới
    ---
    tags:
      - Business Owner
    parameters:
      - in: body
        name: body
        description: Thông tin đăng ký chủ hộ kinh doanh
        required: true
        schema:
          type: object
          required:
            - owner_name
            - email
            - password
            - phone_number
          properties:
            owner_name:
              type: string
              example: "Tran Van Chu"
            business_name:
              type: string
              example: "Tap Hoa Co Ba"
            email:
              type: string
              example: "taphoacoba@gmail.com"
            password:
              type: string
              example: "ChuShop@2026"
            phone_number:
              type: string
              example: "0909123456"
            subscription_plan_id:
              type: integer
              example: 1
              description: ID gói cước muốn đăng ký (1=Basic, 2=Pro)
    responses:
      201:
        description: Đăng ký thành công
    """
    try:
        data = request.get_json()
        result = owner_service.create_owner(data)
        return jsonify({"message": "Thành công", "id": result.owner_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@business_owner_bp.route('/', methods=['GET'])
@token_required
@inject
def get_all_business_owners(owner_service = Provide[Container.business_owner_service]):
    """
    Lấy danh sách chủ doanh nghiệp (Admin Only)
    ---
    tags:
      - Business Owner
    security:
      - Bearer: []
    responses:
      200:
        description: Danh sách chủ hộ
    """
    try:
        owners = owner_service.list_all_owners()
        return jsonify([
            {"id": o.owner_id, "name": o.owner_name, "email": o.email} 
            for o in owners
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500