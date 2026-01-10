from dependency_injector import containers, providers
from infrastructure.databases.mssql import session

# --- IMPORT REPOSITORIES ---
from infrastructure.repositories.access_and_identity_repo.administrator_repository import AdministratorRepository
from infrastructure.repositories.access_and_identity_repo.business_owner_repository import BusinessOwnerRepository
from infrastructure.repositories.access_and_identity_repo.employee_repository import EmployeeRepository
from infrastructure.repositories.access_and_identity_repo.subscription_plan_repository import SubscriptionPlanRepository
from infrastructure.repositories.inventory_repo.product_repository import ProductRepository
from infrastructure.repositories.inventory_repo.unit_repository import UnitRepository
from infrastructure.repositories.inventory_repo.supplier_repository import SupplierRepository
from infrastructure.repositories.inventory_repo.stock_import_repository import StockImportRepository
from infrastructure.repositories.sale_and_finance_repo.customer_repository import CustomerRepository
from infrastructure.repositories.sale_and_finance_repo.order_repository import OrderRepository
from infrastructure.repositories.sale_and_finance_repo.debt_repository import DebtRepository
from infrastructure.repositories.sale_and_finance_repo.account_report_repository import AccountReportRepository
from infrastructure.repositories.ai_core_repo.ai_draft_order_repository import AIDraftOrderRepository
from infrastructure.repositories.ai_core_repo.ai_assistant_repository import AIAssistantRepository

# --- IMPORT SERVICES ---
from services.access_and_identity_service.administrator_service import AdministratorService
from services.access_and_identity_service.business_owner_service import BusinessOwnerService
from services.access_and_identity_service.employee_service import EmployeeService
from services.inventory_service.product_service import ProductService
from services.inventory_service.unit_service import UnitService
from services.inventory_service.supplier_service import SupplierService
from services.sale_and_finance_service.customer_service import CustomerService
from services.sale_and_finance_service.order_service import OrderService
from services.sale_and_finance_service.debt_service import DebtService
from services.sale_and_finance_service.account_report_service import AccountReportService
from services.ai_sore_service.ai_draft_order_service import AIDraftOrderService
from services.ai_sore_service.ai_assistant_service import AIAssistantService

class Container(containers.DeclarativeContainer):
    # Cấu hình session database mặc định cho tất cả repo
    db_session = providers.Object(session)

    # 1. KHAI BÁO REPOSITORIES
    admin_repo = providers.Factory(AdministratorRepository, db_session=db_session)
    owner_repo = providers.Factory(BusinessOwnerRepository, db_session=db_session)
    employee_repo = providers.Factory(EmployeeRepository, db_session=db_session)
    product_repo = providers.Factory(ProductRepository, db_session=db_session)
    unit_repo = providers.Factory(UnitRepository, db_session=db_session)
    supplier_repo = providers.Factory(SupplierRepository, db_session=db_session)
    customer_repo = providers.Factory(CustomerRepository, db_session=db_session)
    order_repo = providers.Factory(OrderRepository, db_session=db_session)
    debt_repo = providers.Factory(DebtRepository, db_session=db_session)
    report_repo = providers.Factory(AccountReportRepository, db_session=db_session)
    draft_repo = providers.Factory(AIDraftOrderRepository, db_session=db_session)
    ai_assistant_repo = providers.Factory(AIAssistantRepository, db_session=db_session)

    # 2. KHAI BÁO SERVICES (Và bơm các repo tương ứng vào)
    admin_service = providers.Factory(AdministratorService, repository=admin_repo)
    owner_service = providers.Factory(BusinessOwnerService, repository=owner_repo)
    employee_service = providers.Factory(EmployeeService, repository=employee_repo)
    product_service = providers.Factory(ProductService, repository=product_repo)
    unit_service = providers.Factory(UnitService, repository=unit_repo)
    supplier_service = providers.Factory(SupplierService, repository=supplier_repo)
    customer_service = providers.Factory(CustomerService, repository=customer_repo)
    debt_service = providers.Factory(DebtService, repository=debt_repo)
    
    # Những service phức tạp cần nhiều "nguyên liệu"
    order_service = providers.Factory(
        OrderService, 
        repository=order_repo, 
        debt_service=debt_service
    )
    
    report_service = providers.Factory(AccountReportService, repository=report_repo)
    
    ai_assistant_service = providers.Factory(
        AIAssistantService, 
        repository=ai_assistant_repo, 
        ai_draft_order_repo=draft_repo
    )

    ai_draft_order_service = providers.Factory(
        AIDraftOrderService,
        draft_repo=draft_repo,
        order_service=order_service,
        customer_repo=customer_repo,
        product_repo=product_repo
    )