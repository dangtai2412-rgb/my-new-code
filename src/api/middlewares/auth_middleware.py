from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

# ⚠️ LƯU Ý: Chuỗi này phải giống hệt SECRET_KEY bên file auth_service.py
# Nếu bên kia bạn để "YOUR_SECRET_KEY" thì bên này cũng phải y chang.
SECRET_KEY = Config.SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 1. Lấy token từ Header (Chuẩn: "Authorization: Bearer <token>")
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1] # Lấy phần chuỗi phía sau chữ Bearer
            else:
                token = auth_header # Trường hợp gửi token trần (ít dùng)

        # 2. Nếu không có token -> Chặn ngay (Lỗi 401)
        if not token:
            return jsonify({'message': 'Token là bắt buộc! (Vui lòng đăng nhập)'}), 401

        try:
            # 3. Giải mã Token
            # Nếu Token hết hạn hoặc bị sửa đổi, hàm này sẽ báo lỗi
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            
            # Lưu thông tin user vào biến request để Controller dùng (nếu cần)
            request.current_user_id = data['user_id']
            request.current_role = data['role']
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token đã hết hạn! Hãy đăng nhập lại.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token không hợp lệ!'}), 401
        except Exception as e:
            return jsonify({'message': 'Lỗi xác thực: ' + str(e)}), 401

        return f(*args, **kwargs)

    return decorated