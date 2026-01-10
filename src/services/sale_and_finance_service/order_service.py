# src/services/sale_and_finance_service/order_service.py
from datetime import datetime
from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel

class OrderService:
    def __init__(self, repository, debt_service):
        self.repository = repository
        self.debt_service = debt_service # Kết nối với DebtService
        

    def create_order(self, data, employee_id):
        # 1. Khởi tạo Header hóa đơn
        payment_method = data.get('payment_method', 'Cash')
        new_order = OrderModel(
            customer_id=data.get('customer_id'),
            employee_id=employee_id,
            order_date=datetime.now(),
            order_status="Completed",
            payment_method=payment_method,
            total_amount=0
        )

        details = []
        final_total = 0

        # 2. Xử lý danh sách sản phẩm (OrderDetail)
        if 'items' in data:
            for item in data['items']:
                line_total = int(item['quantity']) * float(item['unit_price'])
                detail = OrderDetailModel(
                    product_id=item['product_id'],
                    unit_id=item['unit_id'],
                    order_quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    line_total=line_total
                )
                details.append(detail)
                final_total += line_total

        new_order.details = details
        new_order.total_amount = final_total

        # 3. Lưu hóa đơn vào Database
        # Repository cần trả về object đã lưu để lấy được order_id
        saved_order = self.repository.add_order_with_details(new_order)

        # 4. LOGIC TỰ ĐỘNG CẬP NHẬT CÔNG NỢ
        # Nếu thanh toán bằng hình thức ghi nợ, tự động gọi DebtService
        if payment_method == 'Debt' and saved_order:
            self.debt_service.create_debt_from_order(
                order_id=saved_order.order_id,
                customer_id=saved_order.customer_id,
                amount=saved_order.total_amount
            )

        return saved_order