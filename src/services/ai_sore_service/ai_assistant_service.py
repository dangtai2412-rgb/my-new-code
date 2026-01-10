from infrastructure.models.ai_core.ai_assistant_model import AIAssistantModel
import json
class AIAssistantService:
    def __init__(self, repository, ai_draft_order_repo):
        # repository: AIAssistantRepository (quản lý cấu hình AI)
        # ai_draft_order_repo: AIDraftOrderRepository (quản lý các đơn hàng nháp)
        self.repository = repository
        self.ai_draft_order_repo = ai_draft_order_repo

    def update_ai_settings(self, data):
        """
        Cấu hình thông số cho trợ lý AI (Version, Model type)
        """
        version = data.get('version', 'v1.0')
        model_type = data.get('model_type', 'GPT-3.5')

        # Logic: Bạn có thể kiểm tra nếu version trống thì báo lỗi
        if not version:
            raise ValueError("Phiên bản AI không được để trống")

        # Gọi repository để cập nhật vào database
        return self.repository.update_config(version, model_type)

    def get_current_config(self):
        """Lấy cấu hình AI hiện tại"""
        return self.repository.get_latest_config()
    
    def process_order_command(self, text_input):
        """
        Sử dụng LLM để trích xuất thông tin và LƯU vào bảng đơn hàng nháp
        """
        # 1. Định nghĩa Prompt (Bạn đã làm phần này rất tốt)
        prompt = f"""
        Bạn là trợ lý bán hàng cho hộ kinh doanh vật liệu xây dựng. 
        Hãy trích xuất thông tin đơn hàng từ câu lệnh sau: "{text_input}"
        Trả về kết quả dưới dạng JSON duy nhất với các trường:
        - customer_name: Tên khách (string)
        - items: Danh sách sản phẩm (mỗi item gồm: product_name, quantity)
        - payment_method: "Cash" hoặc "Debt" (mặc định "Cash" nếu không nhắc đến)
        """

        # 2. Giả lập gọi LLM (Sau này bạn chỉ cần thay phần này bằng lệnh gọi API thực)
        # Ví dụ kết quả AI trả về:
        ai_extracted_data = {
            "customer_name": "Anh Nam",
            "items": [{"product_name": "Xi măng", "quantity": 2}],
            "payment_method": "Debt"
        }

        # 3. LƯU VÀO DATABASE (Đây là bước quan trọng nhất cho đề tài)
        # Chúng ta lưu vào bảng ai_draft_orders với trạng thái "Pending"
        draft_order = self.ai_draft_order_repo.create_draft({
            "raw_text": text_input,
            "extracted_json": ai_extracted_data,
            "status": "Pending"
        })

        return draft_order
    
    def process_order_command(self, text_input):
        """Trích xuất thông tin và lưu vào danh sách chờ"""
        # (Giữ nguyên logic Prompt ở bước trước của bạn)
        # Giả định kết quả từ LLM trích xuất được:
        ai_extracted_data = {
            "customer_id": 1, # Bạn có thể thêm logic tìm customer_id từ tên
            "items": [{"product_id": 10, "quantity": 5, "unit_price": 50000}],
            "payment_method": "Debt"
        }

        # Lưu vào Database thông qua repo
        return self.draft_repo.create_draft(text_input, ai_extracted_data)
    


    