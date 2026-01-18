from datetime import datetime, timedelta

class AccountReportService:
    # 👇 Chú ý: Tên tham số là 'repository'
    def __init__(self, repository):
        self.repo = repository

    def get_dashboard_stats(self, owner_id):
        # Gọi Repo để lấy data thô, Service chịu trách nhiệm logic nghiệp vụ
        return self.repo.get_dashboard_stats(owner_id)

    def get_revenue_chart(self, owner_id):
        return self.repo.get_revenue_chart(owner_id)

    def get_top_products(self, owner_id):
        return self.repo.get_top_products(owner_id)