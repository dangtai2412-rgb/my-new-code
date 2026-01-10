import json
from config import Config
from infrastructure.models.ai_core.ai_draft_order_model import AIDraftOrderModel
import google.generativeai as genai
import re

class AIDraftOrderService:
    def __init__(self, draft_repo, order_service, customer_repo, product_repo):
        self.draft_repo = draft_repo
        self.order_service = order_service
        self.customer_repo = customer_repo
        self.product_repo = product_repo
        # Khởi tạo Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def create_draft_from_voice(self, voice_text, employee_id):
        """Gọi Gemini để trích xuất thông tin và lưu bản nháp"""
        prompt = f"""
        Bạn là trợ lý bán hàng vật liệu xây dựng chuyên nghiệp. 
        Hãy trích xuất thông tin đơn hàng từ câu sau: "{voice_text}"
        Yêu cầu trả về DUY NHẤT một khối JSON theo cấu trúc:
        {{
            "customer_name": "Tên khách hàng",
            "payment_method": "Cash" hoặc "Debt",
            "items": [
                {{"product_name": "tên sản phẩm", "quantity": số_lượng, "unit": "bao/khối/tấn/viên"}}
            ]
        }}
        Lưu ý: Nếu không nhắc đến thanh toán, mặc định là "Cash".
        """
        try:
            response = self.model.generate_content(prompt)
            # Dùng Regex lấy JSON để tránh văn bản thừa của AI
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            ai_json_str = match.group(0) if match else "{}"
            
            # Lưu vào DB
            return self.draft_repo.create_draft(employee_id, voice_text, ai_json_str)
        except Exception as e:
            raise Exception(f"AI Error: {str(e)}")

    def confirm_and_create_order(self, draft_id, employee_id):
        """BƯỚC QUAN TRỌNG: Chuyển Đơn nháp -> Đơn hàng thật"""
        draft = self.draft_repo.get_by_id(draft_id)
        if not draft: raise ValueError("Draft not found")

        ai_data = json.loads(draft.extracted_json)
        
        # 1. Tìm Customer ID từ tên
        customer = self.customer_repo.get_by_name(ai_data.get('customer_name'))
        
        # 2. Chuẩn bị payload cho OrderService
        order_payload = {
            "customer_id": customer.customer_id if customer else None,
            "payment_method": ai_data.get('payment_method', 'Cash'),
            "items": []
        }

        # 3. Tìm Product ID từ tên AI trích xuất
        for item in ai_data.get('items', []):
            product = self.product_repo.get_by_name(item['product_name'])
            if product:
                order_payload['items'].append({
                    "product_id": product.product_id,
                    "quantity": item['quantity'],
                    "unit_price": product.base_price, # Lấy giá hiện tại trong kho
                    "unit_id": product.unit_id # Có thể cải tiến tìm theo item['unit']
                })

        # 4. Gọi OrderService tạo đơn và hạch toán nợ/báo cáo
        result = self.order_service.create_order(order_payload, employee_id)
        
        if result:
            self.draft_repo.update_status(draft_id, "Confirmed")
        
        return result