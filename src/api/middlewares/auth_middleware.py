from functools import wraps
from flask import request, jsonify
import jwt
from config import Config
from infrastructure.databases import session
from infrastructure.models.access_and_identity.business_owner_model import BusinessOwnerModel
from infrastructure.models.access_and_identity.employee_model import EmployeeModel
from infrastructure.models.access_and_identity.administrator_model import AdministratorModel

# Lấy Secret Key từ Config
SECRET_KEY = Config.SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 1. Lấy token từ Header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
            else:
                token = auth_header

        # 2. Nếu không có token -> Chặn
        if not token:
            return jsonify({'message': 'Vui lòng đăng nhập (Thiếu Token)!'}), 401

        try:
            # 3. Giải mã Token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data['user_id']
            role = data['role']
            
            current_user = None

            # 4. Truy vấn User từ Database dựa theo Role trong Token
            if role == 'owner':
                current_user = session.query(BusinessOwnerModel).filter_by(owner_id=user_id).first()
            elif role == 'employee':
                current_user = session.query(EmployeeModel).filter_by(employee_id=user_id).first()
            elif role == 'admin':
                current_user = session.query(AdministratorModel).filter_by(admin_id=user_id).first()

            if not current_user:
                return jsonify({'message': 'Token không hợp lệ hoặc User không tồn tại!'}), 401

            # 5. Lưu role vào user object để tiện kiểm tra phân quyền sau này (nếu cần)
            current_user.role = role

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Phiên đăng nhập đã hết hạn! Vui lòng đăng nhập lại.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token không hợp lệ!'}), 401
        except Exception as e:
            print(e)
            return jsonify({'message': 'Lỗi xác thực hệ thống'}), 500

        # 6. QUAN TRỌNG NHẤT: Truyền current_user vào hàm Controller
        return f(current_user, *args, **kwargs)

    return decorated