from datetime import date
from infrastructure.models.sale_and_finance.account_report_model import AccountReportModel

class AccountReportService:
    def __init__(self, repository):
        self.repository = repository

    def create_report(self, data):
        # Logic tạo báo cáo (ví dụ: mặc định lấy ngày hiện tại)
        new_report = AccountReportModel(
            owner_id=data['owner_id'],
            report_type=data.get('report_type', 'Daily'),
            report_name=data.get('report_name', f"Report-{date.today()}"),
            generated_date=date.today()
        )
        return self.repository.add(new_report)

    def get_owner_reports(self, owner_id):
        return self.repository.get_by_owner(owner_id)
    def generate_s1_hkd_ledger(self, start_date, end_date):
        """
        Tạo Sổ chi tiết doanh thu (Mẫu S1-HKD)
        """
        raw_data = self.repository.get_revenue_data(start_date, end_date)
        
        ledger = {
            "report_name": "SỔ CHI TIẾT DOANH THU BÁN HÀNG HÓA, DỊCH VỤ",
            "template_code": "Mẫu số S1-HKD",
            "period": f"Từ {start_date} đến {end_date}",
            "data": []
        }

        total_revenue = 0
        for row in raw_data:
            entry = {
                "date": row.order_date.strftime("%d/%m/%Y"),
                "voucher_no": f"HD-{row.order_id}",
                "quantity": row.order_quantity,
                "unit_price": row.unit_price,
                "amount": row.line_total
            }
            ledger["data"].append(entry)
            total_revenue += row.line_total

        ledger["total_revenue"] = total_revenue
        return ledger
    def generate_daily_report(self, owner_id, report_date):
        """Tổng hợp doanh thu, chi phí trong ngày"""
        # Logic gọi repo để tính toán từ bảng Orders và StockImports
        return self.repository.get_report_by_date(owner_id, report_date)