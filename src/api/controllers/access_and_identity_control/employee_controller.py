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
    Tạo nhân viên mới (Dành cho Chủ cửa hàng)
    ---
    tags:
      - Employee
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - employee_name
            - username
            - password
            - owner_id
          properties:
            employee_name:
              type: string
              example: "Le Van Nhan Vien"
            username:
              type: string
              example: "nv_banhang_01"
            password:
              type: string
              example: "Nv123456"
            role:
              type: string
              enum: ["SALES", "INVENTORY", "ACCOUNTANT"]
              example: "SALES"
            owner_id:
              type: integer
              example: 10
              description: ID của chủ cửa hàng quản lý nhân viên này
    responses:
      201:
        description: Tạo nhân viên thành công
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
    ---
    tags:
      - Employee
    security:
      - Bearer: []
    parameters:
      - in: path
        name: owner_id
        type: integer
        required: true
    responses:
      200:
        description: Danh sách nhân viên
    """
    try:
        employees = emp_service.get_employees_by_owner(owner_id)
        return jsonify([
            {"id": e.employee_id, "name": e.employee_name, "role": e.role} 
            for e in employees
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500