# src/services/ai_sore_service/ai_draft_order_service.py
from infrastructure.models.ai_core.ai_draft_order_model import AIDraftOrderModel
import google.generativeai as genai
import json
import re
from config import Config

class AIDraftOrderService:
    def __init__(self, draft_repo, order_service, customer_repo, product_repo):
        self.draft_repo = draft_repo
        self.order_service = order_service
        self.customer_repo = customer_repo 
        self.product_repo = product_repo
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def create_draft_from_voice(self, data):
        recognized_text = data.get('voice_content', '')
        try:
            # 1. Prompt yêu cầu AI trả về JSON chuẩn
            prompt = f"""
            Phân tích câu sau thành JSON đơn hàng: "{recognized_text}"
            Yêu cầu JSON: {{"customer_name": string, "items": [{{"product_name": string, "quantity": number}}], "payment_method": "Cash"|"Debt"}}
            """
            
            response = self.model.generate_content(prompt)
            # Dùng regex để bóc tách JSON (phòng trường hợp AI trả về thêm text giải thích)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            ai_json_str = match.group(0) if match else "{}"
            
            # 2. Lưu vào DB - Quan trọng là phải lưu ai_json_str vào extracted_json
            draft = AIDraftOrderModel(
                employee_id=data.get('employee_id'),
                recognized_content=recognized_text,
                extracted_json=ai_json_str, # LƯU KẾT QUẢ AI VÀO ĐÂY
                source="Voice",
                confirmation_status="Pending"
            )
            return self.draft_repo.create_draft(recognized_text, ai_json_str)
            
        except Exception as e:
            print(f"Lỗi AI: {e}")
            raise Exception("AI không thể phân tích đơn hàng này.")

    def confirm_and_create_order(self, draft_id, employee_id):
        # 1. Lấy đơn nháp
        draft = self.draft_repo.get_by_id(draft_id)
        if not draft or draft.confirmation_status != "Pending":
            raise ValueError("Đơn hàng không hợp lệ.")

        # 2. Giải mã JSON từ AI
        ai_data = json.loads(draft.extracted_json)
        
        # 3. BƯỚC MAPPING ID (Tên -> ID trong Database)
        # Tìm khách hàng theo tên
        customer = self.customer_repo.get_by_name(ai_data.get('customer_name'))
        
        order_payload = {
            "customer_id": customer.customer_id if customer else None,
            "payment_method": ai_data.get('payment_method', 'Cash'),
            "items": []
        }
        
        # Tìm sản phẩm theo tên
        for item in ai_data.get('items', []):
            product = self.product_repo.get_by_name(item['product_name'])
            if product:
                order_payload['items'].append({
                    "product_id": product.product_id,
                    "quantity": item['quantity'],
                    "unit_price": product.base_price, # Lấy giá hiện tại trong kho
                    "unit_id": product.unit_id
                })

        # 4. Gọi OrderService để hạch toán thật
        new_order = self.order_service.create_order(order_payload, employee_id)
        
        if new_order:
            draft.confirmation_status = "Confirmed"
            self.draft_repo.update(draft) # Cập nhật trạng thái đã xác nhận
            
        return new_order