from infrastructure.models import * # Nó phải import hết từ file __init__.py ở bước 1 vào
from .base import Base
from .mssql import engine, session 

def init_db(app):
    with app.app_context():
        # Dòng này là lệnh bắt SQL Server tạo bảng
        Base.metadata.create_all(bind=engine)