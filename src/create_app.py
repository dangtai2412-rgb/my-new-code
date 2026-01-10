from flask import Flask
from config import Config
from api.middleware import setup_middleware
from api.routes import register_routes
from infrastructure.databases import init_db
from app_logging import setup_logging
from cors import init_cors
from dependency_container import Container

def create_app():
    app = Flask(__name__)
    container = Container()
    
    # 2. Đấu dây (Wire) - Đây là bước then chốt để hết lỗi TypeError
    # Bạn phải liệt kê đúng các controller đang dùng @inject
    container.wire(modules=[
        "api.controllers.sale_and_finance_control.order_controller",
        "api.controllers.ai_core_control.ai_draft_order_controller",
        "api.controllers.sale_and_finance_control.customer_controller",
        "api.controllers.inventory_control.product_controller",
        # Thêm các file controller khác của bạn vào đây...
    ])
    
    # Lưu container vào app để Flask quản lý
    app.container = container
    
    
    app.config.from_object(Config)




    setup_logging(app)
    init_db(app)
    init_cors(app)
    setup_middleware(app)
    register_routes(app)

    return app
