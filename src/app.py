from flask import Flask
from flasgger import Swagger
from config import Config
from infrastructure.databases import init_db
from api.routes import register_routes
from api.middleware import setup_middleware
from app_logging import setup_logging
from cors import init_cors
from dependency_container import Container

def create_app():
    app = Flask(__name__)
    
    # 1. Load Config trước tiên
    app.config.from_object(Config)

    # 2. Setup Dependency Injection (QUAN TRỌNG - Đã bị thiếu trước đó)
    container = Container()
    container.wire(modules=[
        "api.controllers.access_and_identity_control.administrator_controller",
        "api.controllers.access_and_identity_control.business_owner_controller",
        "api.controllers.access_and_identity_control.employee_controller",
        "api.controllers.auth_controller",
        "api.controllers.inventory_control.product_controller",
        "api.controllers.inventory_control.unit_controller",
        "api.controllers.inventory_control.supplier_controller",
        "api.controllers.sale_and_finance_control.customer_controller",
        "api.controllers.sale_and_finance_control.order_controller",
        "api.controllers.sale_and_finance_control.debt_controller",
        "api.controllers.sale_and_finance_control.account_report_controller",
        "api.controllers.ai_core_control.ai_draft_order_controller",
        "api.controllers.ai_core_control.ai_assistant_controller",
        "api.controllers.inventory_control.stock_import_detail_controller",
        "api.controllers.inventory_control.stock_import_controller",
        "api.controllers.access_and_identity_control.subscription_plan_controller",
    ])
    app.container = container

    # 3. Setup CORS
    init_cors(app)

    # 4. Setup Logging & Middleware
    setup_logging(app)
    setup_middleware(app)

    # 5. Cấu hình Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/",
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Nhập theo cú pháp: Bearer <token>"
            }
        }
    }
    Swagger(app, config=swagger_config)
    
    # 6. Đăng ký Routes
    register_routes(app)

    # 7. Kết nối Database
    try:
        init_db(app)
        print("✅ Kết nối Database thành công!")
    except Exception as e:
        print(f"❌ Lỗi DB: {e}")

    return app

if __name__ == '__main__':
    app = create_app()
    # Lưu ý: Port là 9999
    print("🚀 Server đang chạy tại: http://localhost:9999")
    print("📄 Tài liệu API (Swagger): http://localhost:9999/docs/")
    app.run(host='0.0.0.0', port=9999, debug=True)