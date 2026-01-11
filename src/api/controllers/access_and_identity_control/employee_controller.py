from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

employee_bp = Blueprint('employee_bp', __name__)

@employee_bp.route('/', methods=['POST'])
@token_required
@inject
def create_new_employee(emp_service = Provide[Container.employee_service]):
    """
    Tạo nhân viên mới
    """
    try:
        data = request.get_json()
        result = emp_service.create_employee(data)
        return jsonify({"message": "Thành công", "id": result.employee_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@employee_bp.route('/owner/<int:owner_id>', methods=['GET'])
@token_required
@inject
def list_employees_by_owner(owner_id, emp_service = Provide[Container.employee_service]):
    """
    Lấy danh sách nhân viên của một chủ sở hữu
    """
    try:
        employees = emp_service.get_employees_by_owner(owner_id)
        return jsonify([
            {"id": e.employee_id, "name": e.employee_name, "role": e.role} 
            for e in employees
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500