from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

business_owner_bp = Blueprint('business_owner_bp', __name__)

@business_owner_bp.route('/', methods=['POST'])
@inject
def register_new_owner(owner_service = Provide[Container.business_owner_service]):
    """
    Tạo chủ cửa hàng mới
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
    Lấy danh sách chủ doanh nghiệp
    """
    try:
        owners = owner_service.list_all_owners()
        return jsonify([
            {"id": o.owner_id, "name": o.owner_name, "email": o.email} 
            for o in owners
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500