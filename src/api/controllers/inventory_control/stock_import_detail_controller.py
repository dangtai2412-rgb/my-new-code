# HÀM THÊM CHI TIẾT (Dùng POST)
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from infrastructure.repositories.inventory_repo.stock_import_repository import StockImportRepository
from services.inventory_service.stock_import_detail_service import StockImportDetailService

stock_import_detail_bp = Blueprint('stock_import_detail_bp', __name__)
stock_repo = StockImportRepository()

service = StockImportDetailService(stock_repo)
@stock_import_detail_bp.route('/', methods=['POST'])
@token_required
def add_detail():
    """
    Thêm chi tiết nhập hàng mới
    ---
    tags: [Inventory Control]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            import_id: {type: integer}
            product_id: {type: integer}
            quantity: {type: integer}
            unit_price: {type: number}
    responses:
      201: {description: "Thành công"}
    """
    data = request.get_json()
    try:
        detail = service.create_detail(data)
        return jsonify({"message": "Thêm thành công", "detail_id": detail.detail_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# HÀM LẤY DANH SÁCH (Dùng GET)
@stock_import_detail_bp.route('/import/<int:import_id>', methods=['GET'])
@token_required
def get_details(import_id):
    """
    Lấy danh sách chi tiết của một phiếu nhập hàng
    ---
    tags: [Inventory Control]
    security: [{BearerAuth: []}]
    parameters:
      - name: import_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: "Danh sách chi tiết"}
    """
    # Logic đúng: Gọi service để lấy dữ liệu thay vì tạo mới
    details = service.get_details_by_import(import_id)
    result = []
    for d in details:
        result.append({
            "product_id": d.product_id,
            "quantity": d.quantity,
            "unit_price": float(d.unit_price)
        })
    return jsonify(result), 200