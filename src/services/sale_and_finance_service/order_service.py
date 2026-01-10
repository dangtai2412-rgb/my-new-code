from datetime import datetime
from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel

class OrderService:
    def __init__(self, repository, debt_service):
        self.repository = repository
        self.debt_service = debt_service

    def create_order(self, data, employee_id):
        payment_method = data.get('payment_method', 'Cash')
        new_order = OrderModel(
            customer_id=data.get('customer_id'),
            employee_id=employee_id,
            order_date=datetime.now(),
            order_status="Completed",
            payment_method=payment_method,
            total_amount=0
        )

        final_total = 0
        details = []
        for item in data.get('items', []):
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

        # Lưu đơn hàng
        saved_order = self.repository.add_order_with_details(new_order)

        # Tự động hạch toán nợ
        if payment_method == 'Debt' and saved_order:
            self.debt_service.create_debt_from_order(
                saved_order.order_id, saved_order.customer_id, saved_order.total_amount
            )

        return saved_order