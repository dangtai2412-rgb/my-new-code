from flask import Blueprint, jsonify
from api.middlewares.auth_middleware import token_required
# Thay vì import từ finance_service chung chung
from services.sale_and_finance_service.account_report_service import AccountReportService
from infrastructure.repositories.sale_and_finance_repo.account_report_repository import AccountReportRepository
from infrastructure.databases.mssql import session
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
account_report_bp = Blueprint('account_report_bp', __name__)

@account_report_bp.route('/', methods=['POST'])
@token_required
@inject
def create_report():
    """
    Tạo báo cáo doanh thu
    ---
    tags: [Reports]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            owner_id: {type: integer, example: 1}
            report_type: {type: string, example: "Monthly"}
            report_name: {type: string, example: "Báo cáo tháng 1"}
    responses:
      201: {description: "Thành công"}
    """
# src/api/controllers/sale_and_finance_control/account_report_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

account_report_bp = Blueprint('account_report_bp', __name__)

@account_report_bp.route('/tt88', methods=['GET'])
@token_required
@inject
def get_tt88_report(report_service = Provide[Container.report_service]):
    """
    Lấy báo cáo Sổ chi tiết doanh thu (Thông tư 88)
    Query param: ?date=YYYY-MM-DD
    """
    try:
        owner_id = getattr(request, 'current_user_id', None)
        report_date = request.args.get('date') # FE gửi ngày muốn xem báo cáo
        
        if not report_date:
            return jsonify({"error": "Vui lòng chọn ngày báo cáo (?date=...)"}), 400
            
        report_data = report_service.generate_daily_report(owner_id, report_date)
        return jsonify(report_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500