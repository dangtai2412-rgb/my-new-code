# src/dependency_container.py
from dependency_injector import containers, providers
from infrastructure.databases.mssql import session

# --- 1. IMPORT REPOSITORIES ---
# Access & Identity
from infrastructure.repositories.access_and_identity_repo.administrator_repository import AdministratorRepository
from infrastructure.repositories.access_and_identity_repo.business_owner_repository import BusinessOwnerRepository
from infrastructure.repositories.access_and_identity_repo.employee_repository import EmployeeRepository
from infrastructure.repositories.access_and_identity_repo.subscription_plan_repository import SubscriptionPlanRepository

# Inventory
from infrastructure.repositories.inventory_repo.product_repository import ProductRepository
from infrastructure.repositories.inventory_repo.unit_repository import UnitRepository
from infrastructure.repositories.inventory_repo.supplier_repository import SupplierRepository
from infrastructure.repositories.inventory_repo.stock_import_repository import StockImportRepository
from infrastructure.repositories.inventory_repo.stock_import_detail_repository import StockImportDetailRepository

# Sale & Finance
from infrastructure.repositories.sale_and_finance_repo.customer_repository import CustomerRepository
from infrastructure.repositories.sale_and_finance_repo.order_repository import OrderRepository
from infrastructure.repositories.sale_and_finance_repo.order_detail_repository import OrderDetailRepository
from infrastructure.repositories.sale_and_finance_repo.debt_repository import DebtRepository
from infrastructure.repositories.sale_and_finance_repo.payment_repository import PaymentRepository
from infrastructure.repositories.sale_and_finance_repo.account_report_repository import AccountReportRepository

# AI Core
from infrastructure.repositories.ai_core_repo.ai_draft_order_repository import AIDraftOrderRepository
from infrastructure.repositories.ai_core_repo.ai_assistant_repository import AIAssistantRepository

# --- 2. IMPORT SERVICES ---
# Access & Identity
from services.access_and_identity_service.administrator_service import AdministratorService
from services.access_and_identity_service.business_owner_service import BusinessOwnerService
from services.access_and_identity_service.employee_service import EmployeeService
from services.access_and_identity_service.subscription_plan_service import SubscriptionPlanService

# Inventory
from services.inventory_service.product_service import ProductService
from services.inventory_service.unit_service import UnitService
from services.inventory_service.supplier_service import SupplierService
from services.inventory_service.stock_import_service import StockImportService
from services.inventory_service.stock_import_detail_service import StockImportDetailService

# Sale & Finance
from services.sale_and_finance_service.customer_service import CustomerService
from services.sale_and_finance_service.order_service import OrderService
from services.sale_and_finance_service.order_detail_service import OrderDetailService
from services.sale_and_finance_service.debt_service import DebtService
from services.sale_and_finance_service.payment_service import PaymentService
from services.sale_and_finance_service.account_report_service import AccountReportService

# AI Core
from services.ai_sore_service.ai_draft_order_service import AIDraftOrderService
from services.ai_sore_service.ai_assistant_service import AIAssistantService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "api.controllers.access_and_identity_control.administrator_controller",
        "api.controllers.access_and_identity_control.business_owner_controller",
        "api.controllers.access_and_identity_control.employee_controller",
        "api.controllers.access_and_identity_control.subscription_plan_controller",
        "api.controllers.access_and_identity_control.auth_controller",
        
        "api.controllers.inventory_control.product_controller",
        "api.controllers.inventory_control.unit_controller",
        "api.controllers.inventory_control.supplier_controller",
        "api.controllers.inventory_control.stock_import_controller",
        "api.controllers.inventory_control.stock_import_detail_controller",
        
        "api.controllers.sale_and_finance_control.customer_controller",
        "api.controllers.sale_and_finance_control.order_controller",
        "api.controllers.sale_and_finance_control.order_detail_controller",
        "api.controllers.sale_and_finance_control.debt_controller",
        "api.controllers.sale_and_finance_control.payment_controller",
        "api.controllers.sale_and_finance_control.account_report_controller",
        
        "api.controllers.ai_core_control.ai_draft_order_controller",
        "api.controllers.ai_core_control.ai_assistant_controller"
    ])

    # Database Session
    db_session = providers.Object(session)

    # ==========================================================
    # 1. REPOSITORIES (Khai báo trước)
    # ==========================================================
    administrator_repo = providers.Factory(AdministratorRepository, db_session=db_session)
    business_owner_repo = providers.Factory(BusinessOwnerRepository, db_session=db_session)
    employee_repo = providers.Factory(EmployeeRepository, db_session=db_session)
    subscription_plan_repo = providers.Factory(SubscriptionPlanRepository, db_session=db_session)

    product_repo = providers.Factory(ProductRepository, db_session=db_session)
    unit_repo = providers.Factory(UnitRepository, db_session=db_session)
    supplier_repo = providers.Factory(SupplierRepository, db_session=db_session)
    stock_import_repo = providers.Factory(StockImportRepository, db_session=db_session)
    stock_import_detail_repo = providers.Factory(StockImportDetailRepository, db_session=db_session)

    customer_repo = providers.Factory(CustomerRepository, db_session=db_session)
    order_repo = providers.Factory(OrderRepository, db_session=db_session)
    order_detail_repo = providers.Factory(OrderDetailRepository, db_session=db_session)
    debt_repo = providers.Factory(DebtRepository, db_session=db_session)
    payment_repo = providers.Factory(PaymentRepository, db_session=db_session)
    account_report_repo = providers.Factory(AccountReportRepository, db_session=db_session)

    ai_draft_order_repo = providers.Factory(AIDraftOrderRepository, db_session=db_session)
    ai_assistant_repo = providers.Factory(AIAssistantRepository, db_session=db_session)

    # ==========================================================
    # 2. SERVICES (Khai báo sau, dùng Repository ở trên)
    # ==========================================================
    
    # --- Access & Identity ---
    administrator_service = providers.Factory(AdministratorService, repository=administrator_repo)
    business_owner_service = providers.Factory(BusinessOwnerService, repository=business_owner_repo)
    employee_service = providers.Factory(EmployeeService, repository=employee_repo)
    subscription_plan_service = providers.Factory(SubscriptionPlanService, repository=subscription_plan_repo)

    # --- Inventory ---
    product_service = providers.Factory(ProductService, repository=product_repo)
    unit_service = providers.Factory(UnitService, repository=unit_repo)
    supplier_service = providers.Factory(SupplierService, repository=supplier_repo)
    stock_import_service = providers.Factory(StockImportService, repository=stock_import_repo)
    stock_import_detail_service = providers.Factory(StockImportDetailService, repository=stock_import_detail_repo)

    # --- Sale & Finance ---
    customer_service = providers.Factory(CustomerService, repository=customer_repo)
    
    debt_service = providers.Factory(DebtService, repository=debt_repo)
    
    payment_service = providers.Factory(
        PaymentService, 
        repository=payment_repo,
        debt_repository=debt_repo
    )
    
    order_detail_service = providers.Factory(OrderDetailService, repository=order_detail_repo)
    
    # Order Service cần cả OrderRepo và DebtService (để tự động ghi nợ)
    order_service = providers.Factory(
        OrderService,
        repository=order_repo,
        debt_service=debt_service
    )

    report_service = providers.Factory(AccountReportService, repository=account_report_repo)

    # --- AI Core ---
    # AI Assistant cần AI Repo và AI Draft Repo
    ai_assistant_service = providers.Factory(
        AIAssistantService,
        repository=ai_assistant_repo,
        ai_draft_order_repo=ai_draft_order_repo
    )

    # AI Draft Order cần rất nhiều thứ để kiểm tra tên sản phẩm, khách hàng
    ai_draft_order_service = providers.Factory(
        AIDraftOrderService,
        draft_repo=ai_draft_order_repo,
        order_service=order_service,
        customer_repo=customer_repo,
        product_repo=product_repo
    )