from datetime import datetime
from infrastructure.models.sale_and_finance.return_order_model import ReturnOrderModel
from infrastructure.models.sale_and_finance.return_order_detail_model import ReturnOrderDetailModel
from infrastructure.databases import session

class ReturnOrderService:
    def __init__(self, product_repository, return_order_repository):
        self.product_repository = product_repository
        self.return_order_repository = return_order_repository

    def create_return(self, data, owner_id):
        # 1. Tạo phiếu trả
        code = f"RO-{int(datetime.now().timestamp())}"
        new_return = ReturnOrderModel(
            return_code=code,
            customer_id=data['customer_id'],
            order_id=data.get('order_id'),
            reason=data.get('reason', ''),
            owner_id=owner_id,
            total_refund=0
        )
        session.add(new_return)
        session.flush()

        total_money = 0
        
        # 2. Xử lý từng món hàng
        for item in data['details']:
            product = self.product_repository.get_by_id(item['product_id'])
            if not product: continue

            # Tạo chi tiết trả
            detail = ReturnOrderDetailModel(
                return_id=new_return.return_id,
                product_id=product.product_id,
                quantity=item['quantity'],
                refund_price=item['refund_price']
            )
            session.add(detail)

            # 🚀 QUAN TRỌNG: Khách trả hàng -> Kho TĂNG lên
            product.stock_quantity += item['quantity']
            
            # Tính tổng tiền hoàn
            total_money += (item['quantity'] * item['refund_price'])

        new_return.total_refund = total_money
        
        session.commit()
        return new_return

    def get_history(self, owner_id):
        return self.return_order_repository.get_all(owner_id)