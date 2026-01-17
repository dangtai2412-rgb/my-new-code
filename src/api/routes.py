#from api.controllers.todo_controller import bp as todo_bp
from api.controllers.access_and_identity_control.business_owner_controller import business_owner_bp
from api.controllers.access_and_identity_control.employee_controller import employee_bp
from api.controllers.inventory_control.product_controller import product_bp
from api.controllers.access_and_identity_control.administrator_controller import admin_bp
from api.controllers.sale_and_finance_control.customer_controller import customer_bp
from api.controllers.access_and_identity_control.subscription_plan_controller import subscription_plan_bp
from api.controllers.inventory_control.unit_controller import unit_bp
from api.controllers.sale_and_finance_control.order_controller import order_bp
from api.controllers.sale_and_finance_control.order_detail_controller import order_detail_bp
from api.controllers.sale_and_finance_control.debt_controller import debt_bp
from api.controllers.sale_and_finance_control.payment_controller import payment_bp
from api.controllers.sale_and_finance_control.account_report_controller import account_report_bp
from api.controllers.ai_core_control.ai_assistant_controller import ai_assistant_bp
from api.controllers.ai_core_control.ai_draft_order_controller import ai_draft_order_bp
from api.controllers.auth_controller import auth_bp
from api.controllers.inventory_control.supplier_controller import supplier_bp
from api.controllers.inventory_control.stock_import_controller import stock_import_bp
from api.controllers.inventory_control.stock_import_detail_controller import stock_import_detail_bp
from api.controllers.inventory_control.category_controller import category_bp
from api.controllers.inventory_control.inventory_check_controller import inventory_check_bp
from api.controllers.sale_and_finance_control.return_order_controller import return_order_bp

def register_routes(app):
    # Đăng ký todo ở đây (vì đã xóa ở app.py)
    #app.register_blueprint(todo_bp, url_prefix='/todos')
    # Đăng ký Business Owner
    app.register_blueprint(business_owner_bp, url_prefix='/business-owners')


    app.register_blueprint(employee_bp, url_prefix='/employees')

    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(admin_bp, url_prefix='/administrators')
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(subscription_plan_bp, url_prefix='/subscription-plans')

    app.register_blueprint(unit_bp, url_prefix='/units')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(order_detail_bp, url_prefix='/order-details')
    app.register_blueprint(debt_bp, url_prefix='/debts')
    app.register_blueprint(payment_bp, url_prefix='/payments')
    app.register_blueprint(account_report_bp, url_prefix='/account-reports')
    app.register_blueprint(ai_assistant_bp, url_prefix='/ai-assistants')
    app.register_blueprint(ai_draft_order_bp, url_prefix='/ai-draft-orders')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(supplier_bp, url_prefix='/suppliers')
    app.register_blueprint(stock_import_bp, url_prefix='/stock-imports')
    app.register_blueprint(stock_import_detail_bp, url_prefix='/stock-import-details')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(inventory_check_bp, url_prefix='/inventory-checks')
    app.register_blueprint(return_order_bp, url_prefix='/return-orders')










