# src/api/controllers/inventory_control/product_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

product_bp = Blueprint('product_bp', __name__)

# --- XÓA KHỞI TẠO THỦ CÔNG repo/service Ở ĐÂY ---

@product_bp.route('/', methods=['POST'])
@token_required
@inject
def create_new_product(product_service = Provide[Container.product_service]):
    """
    Thêm sản phẩm mới
    ---
    tags: [Inventory]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          required: [product_name, selling_price]
          properties:
            product_name: {type: string, example: "Gạch men 60x60"}
            selling_price: {type: number, example: 150000}
            stock_quantity: {type: integer, example: 100}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        data['owner_id'] = getattr(request, 'current_user_id', None)
        product = product_service.create_product(data)
        return jsonify({"message": "Success", "product_id": product.product_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@product_bp.route('/', methods=['GET'])
@token_required
@inject
def list_products_by_owner(product_service = Provide[Container.product_service]):
    """
    Lấy danh sách sản phẩm
    ---
    tags: [Inventory]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Thành công"}
    """
    try:
        owner_id = getattr(request, 'current_user_id', None)
        products = product_service.get_products_by_owner(owner_id)
        result = [{"id": p.product_id, "name": p.product_name, "price": p.selling_price} for p in products]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@product_bp.route('/<int:product_id>', methods=['PUT'])
@token_required
@inject
def update_product(product_id, product_service = Provide[Container.product_service]):
    """Cập nhật thông tin sản phẩm"""
    try:
        data = request.get_json()
        result = product_service.update_product(product_id, data)
        return jsonify({"message": "Updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@token_required
@inject
def delete_product(product_id, product_service = Provide[Container.product_service]):
    """Xóa sản phẩm"""
    try:
        product_service.delete_product(product_id)
        return jsonify({"message": "Deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400