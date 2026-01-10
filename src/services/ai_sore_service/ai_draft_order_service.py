from infrastructure.models.ai_core.ai_draft_order_model import AIDraftOrderModel
import google.generativeai as genai
class AIDraftOrderService:
    def __init__(self, repository):
        self.repository = repository

    def create_draft_from_voice(self, data):
        # Giả lập logic AI phân tích giọng nói thành văn bản
        recognized_text = data.get('voice_content', '')
        try:
            prompt = f"Phân tích câu sau thành dữ liệu đơn hàng: {recognized_text}"
            
            # Gọi API với tham số timeout để tránh lỗi Code 4
            response = self.model.generate_content(
                prompt,
                request_options={"timeout": 600} # Đợi tối đa 10 phút
            )
            ai_result = response.text
            print(f"AI Response: {ai_result}") # Để bạn debug
            
        except Exception as e:
            # Nếu bị timeout hoặc lỗi, log ra để biết và báo lỗi thân thiện
            print(f"Lỗi kết nối Gemini: {e}")
            raise Exception("AI đang bận xử lý dữ liệu giọng nói, vui lòng thử lại sau!")
        
        draft = AIDraftOrderModel(
            employee_id=data.get('employee_id'),
            customer_id=data.get('customer_id'),
            ai_id=1, # Giả sử dùng AI Assistant ID 1
            recognized_content=recognized_text,
            source="Voice",
            confirmation_status="Pending"
        )
        return self.repository.add(draft)