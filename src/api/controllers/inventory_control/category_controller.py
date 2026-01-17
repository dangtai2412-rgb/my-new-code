from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from api.schemas.category import CategorySchema
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

category_bp = Blueprint('category_bp', __name__)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

@category_bp.route('/', methods=['GET'])
@token_required
@inject
def get_categories(current_user, service=Provide[Container.category_service]):
    """
    Lấy danh sách danh mục
    ---
    tags:
      - Inventory - Categories
    security:
      - Bearer: []
    responses:
      200:
        description: Danh sách danh mục thành công
    """
    categories = service.get_categories(current_user.owner_id)
    return jsonify(categories_schema.dump(categories)), 200

@category_bp.route('/', methods=['POST'])
@token_required
@inject
def create_category(current_user, service=Provide[Container.category_service]):
    """
    Tạo danh mục mới
    ---
    tags:
      - Inventory - Categories
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        description: Thông tin danh mục cần tạo
        required: true
        schema:
          type: object
          required:
            - category_name
          properties:
            category_name:
              type: string
              example: "Vật liệu xây dựng thô"
              description: Tên danh mục (Bắt buộc)
            description:
              type: string
              example: "Gồm cát, đá, xi măng, gạch..."
              description: Mô tả thêm (Không bắt buộc)
    responses:
      201:
        description: Tạo thành công
      400:
        description: Dữ liệu đầu vào không hợp lệ
    """
    data = request.get_json()
    
    # Validate dữ liệu đầu vào
    errors = category_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    new_cat = service.create_category(data, current_user.owner_id)
    return jsonify(category_schema.dump(new_cat)), 201

@category_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@inject
def delete_category(id, current_user, service=Provide[Container.category_service]):
    """
    Xóa danh mục
    ---
    tags:
      - Inventory - Categories
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID của danh mục cần xóa
    responses:
      200:
        description: Đã xóa thành công
      404:
        description: Không tìm thấy danh mục
    """
    success = service.delete_category(id)
    if success:
        return jsonify({"message": "Đã xóa danh mục"}), 200
    return jsonify({"error": "Không tìm thấy danh mục hoặc không thuộc quyền sở hữu"}), 404