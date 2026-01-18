from flask import Blueprint, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

account_report_bp = Blueprint('account_report_bp', __name__)

@account_report_bp.route('/dashboard', methods=['GET'])
@token_required
@inject
def get_dashboard_stats(current_user, service=Provide[Container.account_report_service]):
    """
    Lấy số liệu tổng quan Dashboard
    ---
    tags:
      - Reporting
    security:
      - Bearer: []
    responses:
      200:
        description: Trả về doanh thu, đơn hàng, cảnh báo kho
    """
    stats = service.get_dashboard_stats(current_user.owner_id)
    return jsonify(stats), 200

@account_report_bp.route('/chart', methods=['GET'])
@token_required
@inject
def get_revenue_chart(current_user, service=Provide[Container.account_report_service]):
    """
    Lấy dữ liệu biểu đồ doanh thu 7 ngày
    ---
    tags:
      - Reporting
    security:
      - Bearer: []
    responses:
      200:
        description: Mảng dữ liệu ngày và doanh thu
    """
    chart_data = service.get_revenue_chart(current_user.owner_id)
    return jsonify(chart_data), 200

@account_report_bp.route('/top-products', methods=['GET'])
@token_required
@inject
def get_top_products(current_user, service=Provide[Container.account_report_service]):
    """
    Lấy Top 5 sản phẩm bán chạy
    ---
    tags:
      - Reporting
    security:
      - Bearer: []
    """
    products = service.get_top_products(current_user.owner_id)
    return jsonify(products), 200