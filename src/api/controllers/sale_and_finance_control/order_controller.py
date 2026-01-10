# src/api/controllers/sale_and_finance_control/order_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/', methods=['POST'])
@token_required
@inject
def post_order(order_service = Provide[Container.order_service]): # Sửa lỗi thiếu tham số
    """
    Tạo đơn hàng (Tự động trừ kho & hạch toán nợ)
    """
    try:
        data = request.get_json()
        # Lấy ID nhân viên thực hiện đơn hàng từ token
        employee_id = getattr(request, 'current_user_id', None)
        
        result = order_service.create_order(data, employee_id)
        return jsonify({
            "message": "Tạo đơn hàng thành công", 
            "order_id": result.order_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400