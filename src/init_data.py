import sys
import os
from werkzeug.security import generate_password_hash

# Thêm đường dẫn để python tìm thấy các module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from infrastructure.databases import session
from infrastructure.models.access_and_identity.business_owner_model import BusinessOwnerModel
from infrastructure.models.user_model import UserModel
# Import thêm AdministratorModel nếu cần

app = create_app()

def init_db_data():
    with app.app_context():
        print("--- BẮT ĐẦU TẠO TÀI KHOẢN MẪU ---")

        # 1. Tạo Business Owner (Chủ cửa hàng)
        # Kiểm tra xem email đã tồn tại chưa
        existing_user = session.query(UserModel).filter_by(email="shop@gmail.com").first()
        
        if not existing_user:
            # Tạo User trước
            new_user = UserModel(
                email="shop@gmail.com",
                password_hash=generate_password_hash("123456"), # Mật khẩu là 123456
                full_name="Chủ Shop Demo",
                role="BUSINESS_OWNER",
                is_active=True,
                phone_number="0987654321"
            )
            session.add(new_user)
            session.commit() # Commit để lấy user_id

            # Tạo Business Owner gắn với User đó
            new_owner = BusinessOwnerModel(
                user_id=new_user.user_id,
                business_name="Cửa hàng tạp hóa Demo",
                tax_id="MST001",
                address="Hà Nội"
            )
            session.add(new_owner)
            session.commit()
            print("✅ Đã tạo tài khoản: shop@gmail.com / 123456")
        else:
            print("⚠️ Tài khoản shop@gmail.com đã tồn tại!")

        print("--- HOÀN TẤT ---")

if __name__ == "__main__":
    init_db_data()