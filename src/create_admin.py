from create_app import create_app
from infrastructure.databases import session # <--- Import 'session' thay vì 'db'
from infrastructure.models.access_and_identity.administrator_model import AdministratorModel
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # 1. Tạo thông tin Admin
    username = "admin"
    password_raw = "123456"
    
    # 2. Kiểm tra
    existing_user = session.query(AdministratorModel).filter_by(username=username).first() # Sửa db.session -> session
    
    if existing_user:
        print(f"❌ Tài khoản '{username}' đã tồn tại rồi!")
    else:
        # 3. Mã hóa pass
        password_hash = generate_password_hash(password_raw)
        
        # 4. Lưu vào DB
        new_admin = AdministratorModel(
            username=username,
            password_hash=password_hash,
            email="admin@bizflow.com",
            full_name="Super Admin"
        )
        session.add(new_admin)    # Sửa db.session.add -> session.add
        session.commit()          # Sửa db.session.commit -> session.commit
        print(f"✅ Đã tạo tài khoản thành công! User: {username} / Pass: {password_raw}")