from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from infrastructure.repositories.inventory_repo.supplier_repository import SupplierRepository
from services.inventory_service.supplier_service import SupplierService

supplier_bp = Blueprint('supplier_bp', __name__)
supplier_repo = SupplierRepository()
supplier_service = SupplierService(supplier_repo)

@supplier_bp.route('/', methods=['POST'])
@token_required
def add_supplier():
    """
    Thêm nhà cung cấp mới
    ---
    tags: [Suppliers]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            supplier_name: {type: string, example: "Công ty ABC"}
            phone_number: {type: string, example: "0901234567"}
            tax_code: {type: string, example: "123456789"}
    responses:
      201: {description: "Thành công"}
    """
    data = request.get_json() # Chuyển xuống dưới Docstring
    owner_id = request.current_user_id
    try:
        supplier = supplier_service.create_supplier(data, owner_id)
        return jsonify({"message": "Thêm nhà cung cấp thành công", "id": supplier.supplier_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@supplier_bp.route('/', methods=['GET'])
@token_required
def get_suppliers():
    """
    Lấy danh sách nhà cung cấp
    ---
    tags: [Suppliers]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Danh sách nhà cung cấp"}
    """
    
    owner_id = request.current_user_id
    suppliers = supplier_service.get_suppliers(owner_id)
    result = []
    for s in suppliers:
        result.append({
            "supplier_id": s.supplier_id,
            "supplier_name": s.supplier_name,
            "phone_number": s.phone_number,
            "tax_code": s.tax_code
        })
    return jsonify(result), 200