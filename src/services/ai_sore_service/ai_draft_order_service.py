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

    def create_draft_from_voice(self, voice_text, employee_id):
        prompt = f"Phân tích câu sau thành JSON đơn hàng: '{voice_text}'. Trả về JSON: {{\"customer_name\": string, \"items\": [{{\"product_name\": string, \"quantity\": number}}], \"payment_method\": \"Cash\"|\"Debt\"}}"
        try:
            response = self.model.generate_content(prompt)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            ai_json = match.group(0) if match else "{}"
            return self.draft_repo.create_draft(employee_id, voice_text, ai_json)
        except Exception as e:
            raise Exception(f"AI Error: {str(e)}")

    def confirm_and_create_order(self, draft_id, employee_id):
        draft = self.draft_repo.get_by_id(draft_id)
        ai_data = json.loads(draft.extracted_json)
        customer = self.customer_repo.get_by_name(ai_data.get('customer_name'))
        
        order_payload = {
            "customer_id": customer.customer_id if customer else None,
            "payment_method": ai_data.get('payment_method', 'Cash'),
            "items": []
        }
        for item in ai_data.get('items', []):
            product = self.product_repo.get_by_name(item['product_name'])
            if product:
                order_payload['items'].append({
                    "product_id": product.product_id,
                    "quantity": item['quantity'],
                    "unit_price": product.base_price,
                    "unit_id": product.unit_id
                })
        result = self.order_service.create_order(order_payload, employee_id)
        if result: self.draft_repo.update_status(draft_id, "Confirmed")
        return result