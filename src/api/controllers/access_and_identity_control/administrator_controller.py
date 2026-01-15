from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/', methods=['POST'])
@inject
def create(admin_service = Provide[Container.administrator_service]):
    """
    Tạo Admin mới (System Admin)
    ---
    tags:
      - Administrator
    parameters:
      - in: body
        name: body
        description: Thông tin tạo tài khoản Admin
        required: true
        schema:
          type: object
          required:
            - username
            - password
            - email
          properties:
            username:
              type: string
              example: "superadmin"
            password:
              type: string
              example: "Secret@123"
            email:
              type: string
              example: "admin@bizflowa.com"
            full_name:
              type: string
              example: "Nguyen Van Quan Tri"
    responses:
      201:
        description: Tạo thành công
      400:
        description: Dữ liệu không hợp lệ
    """
    try:
        data = request.get_json()
        result = admin_service.create_admin(data)
        return jsonify({"message": "Thành công", "id": result.admin_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@admin_bp.route('/', methods=['GET'])
@token_required
@inject
def list_admins(admin_service = Provide[Container.administrator_service]):
    """
    Lấy danh sách Admin
    ---
    tags:
      - Administrator
    security:
      - Bearer: []
    responses:
      200:
        description: Danh sách admin
    """
    try:
        admins = admin_service.get_all_admins()
        return jsonify([{"id": a.admin_id, "name": a.admin_name} for a in admins]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500