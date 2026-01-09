# File: src/create_app.py
from create_app import create_app
from infrastructure.databases import db
# Import đúng model Admin của bạn
from infrastructure.models.access_and_identity.administrator_model import AdministratorModel
from werkzeug.security import generate_password_hash
from config import Config
app = create_app()

with app.app_context():
    # 1. Tạo thông tin Admin mẫu
    username = "admin"
    password_raw = "123456" # Mật khẩu bạn muốn đặt
    
    # 2. Kiểm tra xem đã có chưa
    existing_user = db.session.query(AdministratorModel).filter_by(username=username).first()
    
    if existing_user:
        print(f"❌ Tài khoản '{username}' đã tồn tại rồi!")
    else:
        # 3. Mã hóa mật khẩu (Quan trọng nhất)
        password_hash = generate_password_hash(password_raw)
        
        # 4. Lưu vào DB
        new_admin = AdministratorModel(
            username=username,
            password_hash=password_hash,
            email="admin@bizflow.com",
            full_name="Super Admin"
        )
        db.session.add(new_admin)
        db.session.commit()
        print(f"✅ Đã tạo tài khoản thành công! User: {username} / Pass: {password_raw}")