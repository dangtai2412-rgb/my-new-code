from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from api.schemas.expense import ExpenseSchema
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

expense_bp = Blueprint('expense_bp', __name__)
expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)

@expense_bp.route('/', methods=['POST'])
@token_required
@inject
def create_expense(current_user, service=Provide[Container.expense_service]):
    """
    Tạo phiếu chi mới
    ---
    tags:
      - Sale & Finance - Expenses
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        description: Thông tin chi phí
        required: true
        schema:
          type: object
          required:
            - expense_name
            - amount
          properties:
            expense_name:
              type: string
              example: "Tiền điện tháng 1/2026"
            amount:
              type: number
              example: 1500000
            category:
              type: string
              example: "Điện nước"
            note:
              type: string
              example: "Đã thanh toán qua CK"
    responses:
      201:
        description: Tạo thành công
    """
    data = request.get_json()
    errors = expense_schema.validate(data)
    if errors:
        return jsonify(errors), 400
        
    new_expense = service.create_expense(data, current_user.owner_id)
    return jsonify(expense_schema.dump(new_expense)), 201

@expense_bp.route('/', methods=['GET'])
@token_required
@inject
def get_expenses(current_user, service=Provide[Container.expense_service]):
    """
    Lấy danh sách chi phí
    ---
    tags:
      - Sale & Finance - Expenses
    security:
      - Bearer: []
    responses:
      200:
        description: Danh sách chi phí
    """
    expenses = service.get_expenses(current_user.owner_id)
    return jsonify(expenses_schema.dump(expenses)), 200

@expense_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@inject
def delete_expense(id, current_user, service=Provide[Container.expense_service]):
    """Xóa phiếu chi"""
    if service.delete_expense(id):
        return jsonify({"message": "Đã xóa"}), 200
    return jsonify({"error": "Không tìm thấy"}), 404