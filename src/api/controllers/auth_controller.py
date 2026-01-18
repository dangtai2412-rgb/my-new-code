from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.auth_service import AuthService
import json

auth_bp = Blueprint('auth_bp', __name__)

# --- SỬA LỖI 1: Đưa Route lên TRÊN, Inject xuống DƯỚI ---
@auth_bp.route('/login', methods=['POST'])
@inject
def login_system(
    auth_service: AuthService = Provide[Container.auth_service]
):
    """
    Đăng nhập hệ thống
    ---
    tags:
      - Auth
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Thông tin đăng nhập
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "admin01"
            password:
              type: string
              example: "123456"
    responses:
      200:
        description: Thành công
      400:
        description: Thiếu thông tin
      401:
        description: Sai thông tin
    """
    # --- DEBUG: In ra tất cả những gì server nhận được ---
    print(f"--- DEBUG LOGIN REQUEST ---")
    print(f"Headers: {request.headers}")
    raw_data = request.get_data(as_text=True)
    print(f"Raw Body: {raw_data}")

    # --- SỬA LỖI 2: Dùng force=True để ép đọc JSON dù header có sai ---
    data = request.get_json(silent=True, force=True)
    
    # Fallback: Nếu JSON null thì thử parse thủ công từ text
    if not data and raw_data:
        try:
            data = json.loads(raw_data)
        except:
            pass
            
    # Fallback: Nếu vẫn null thì thử lấy Form Data
    if not data:
        data = request.form.to_dict()

    print(f"Parsed Data: {data}") # Xem kết quả cuối cùng server hiểu là gì

    # Kiểm tra dữ liệu
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "error": "Tên đăng nhập và mật khẩu là bắt buộc",
            "received_raw": raw_data, # Trả về cho bạn xem server thấy gì
            "parsed_data": data
        }), 400

    try:
        # Gọi Service xử lý
        result = auth_service.login(data['username'], data['password'])
        return jsonify(result), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401
    except Exception as e:
        print(f"SYSTEM ERROR: {e}")
        return jsonify({"error": "Lỗi hệ thống: " + str(e)}), 500