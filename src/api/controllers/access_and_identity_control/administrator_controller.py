from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/', methods=['POST'])
@inject
def create(admin_service = Provide[Container.administrator_service]):
    """
    Tạo Admin mới
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
    """
    try:
        admins = admin_service.get_all_admins()
        # Giả sử model có to_dict hoặc bạn tự map
        return jsonify([{"id": a.admin_id, "name": a.admin_name} for a in admins]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500