from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from infrastructure.repositories.inventory_repo.stock_import_repository import StockImportRepository
from services.inventory_service.stock_import_service import StockImportService

stock_import_bp = Blueprint('stock_import_bp', __name__)
stock_repo = StockImportRepository()
stock_service = StockImportService(stock_repo)

@stock_import_bp.route('/', methods=['POST'])
@token_required
def import_goods():
    """
    Tạo phiếu nhập hàng (Tăng tồn kho tự động)
    ---
    tags: [Inventory Control]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            supplier_id: {type: integer, example: 1}
            items:
              type: array
              items:
                type: object
                properties:
                  product_id: {type: integer, example: 1}
                  quantity: {type: integer, example: 10}
                  unit_price: {type: number, example: 50000}
    responses:
      201: {description: "Nhập hàng thành công"}
    """
    data = request.get_json()
    owner_id = request.current_user_id
    
    
    try:
        result = stock_service.create_stock_import(data, owner_id)
        return jsonify({
            "message": "Nhập hàng và cập nhật kho thành công", 
            "import_id": result.import_id,
            "total_amount": float(result.total_amount)
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400