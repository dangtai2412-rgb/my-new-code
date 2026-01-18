from flask import Blueprint, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.account_report_service import AccountReportService
from api.middlewares.auth_middleware import token_required

account_report_bp = Blueprint('account_report_bp', __name__)

@account_report_bp.route('/dashboard', methods=['GET'])
@token_required
@inject
def get_dashboard_stats(current_user, service: AccountReportService = Provide[Container.account_report_service]):
    try:
        # Lấy owner_id từ token
        owner_id = getattr(current_user, 'owner_id', None)
        data = service.get_dashboard_stats(owner_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Làm tương tự cho /chart và /top-products (dùng service.get_revenue_chart...)