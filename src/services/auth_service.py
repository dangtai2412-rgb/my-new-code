from werkzeug.security import check_password_hash
import jwt
import datetime
from config import Config
class AuthService:
    def __init__(self, admin_repo, owner_repo, emp_repo):
        self.admin_repo = admin_repo
        self.owner_repo = owner_repo
        self.emp_repo = emp_repo

    def login(self, username, password):
        # 1. Quét Admin -> 2. Quét Owner -> 3. Quét Employee
        user = self.admin_repo.get_by_name(username)
        role = "admin"
        id_field = "admin_id"
        
        if not user:
            user = self.owner_repo.get_by_name(username)
            role = "owner"
            id_field = "owner_id"
            
        if not user:
            user = self.emp_repo.get_by_name(username)
            role = "employee"
            id_field = "employee_id"

        # 2. Kiểm tra mật khẩu và tạo Token
        if user and check_password_hash(user.password, password):
            # Lấy ID thực tế từ Model (ví dụ: owner_id hoặc employee_id)
            user_id = getattr(user, id_field)
            
            payload = {
                'user_id': user_id,
                'role': role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            
            # Lưu ý: "YOUR_SECRET_KEY" nên để trong file config.py
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
            
            return {
                "token": token, 
                "role": role, 
                "user_id": user_id,
                "username": username
            }
            
        raise ValueError("Tài khoản hoặc mật khẩu không chính xác")