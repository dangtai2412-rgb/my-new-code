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
    
    # Liệt kê chính xác module controller của bạn
    container.wire(modules=[
        "api.controllers.sale_and_finance_control.order_controller",
        "api.controllers.ai_core_control.ai_draft_order_controller",
        "api.controllers.sale_and_finance_control.account_report_controller"
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
