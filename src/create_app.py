from flask import Flask, app
from config import Config
from api.middleware import setup_middleware
from api.routes import register_routes
from infrastructure.databases import init_db
from app_logging import setup_logging
from cors import init_cors
from dependency_container import Container

def create_app():
    app = Flask(__name__)
    # Trong hàm create_app():
    container = Container()
    container.wire(modules=[
        "api.controllers.access_and_identity_control.administrator_controller",
        "api.controllers.access_and_identity_control.business_owner_controller",
        "api.controllers.access_and_identity_control.employee_controller",
        "api.controllers.auth_controller", # Đã sửa đường dẫn này cho đúng với file thực tế
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
        "api.controllers.inventory_control.stock_import_controller" 
        # ĐÃ XÓA DÒNG "" DƯ THỪA TẠI ĐÂY
    ])
    app.container = container
    

    
    app.config.from_object(Config)




    setup_logging(app)
    init_db(app)
    init_cors(app)
    setup_middleware(app)
    register_routes(app)

    return app
