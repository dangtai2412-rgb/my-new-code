# src/dependency_container.py
# ...
from dependency_injector import containers, providers
# CẦN BỔ SUNG CÁC DÒNG IMPORT DƯỚI ĐÂY:
from services.sale_and_finance_service.order_service import OrderService
from services.sale_and_finance_service.debt_service import DebtService
from infrastructure.repositories.sale_and_finance_repo.order_repository import OrderRepository
from infrastructure.repositories.sale_and_finance_repo.debt_repository import DebtRepository
from services.sale_and_finance_service.account_report_service import AccountReportService
from infrastructure.repositories.sale_and_finance_repo.order_repository import OrderRepository
from infrastructure.repositories.sale_and_finance_repo.account_report_repository import AccountReportRepository
from infrastructure.repositories.ai_core_repo.ai_draft_order_repository import AIDraftOrderRepository
from services.ai_sore_service.ai_draft_order_service import AIDraftOrderService
from infrastructure.repositories.ai_core_repo.ai_assistant_repository import AIAssistantRepository
from services.ai_sore_service.ai_assistant_service import AIAssistantService
from infrastructure.repositories.sale_and_finance_repo.customer_repository import CustomerRepository
from infrastructure.repositories.inventory_repo.product_repository import ProductRepository





class Container(containers.DeclarativeContainer):
    # Khai báo các Repository
    order_repo = providers.Factory(OrderRepository)
    debt_repo = providers.Factory(DebtRepository)
    report_repo = providers.Factory(AccountReportRepository)
    draft_repo = providers.Factory(AIDraftOrderRepository)
    ai_assistant_repo = providers.Factory(AIAssistantRepository)
    customer_repo = providers.Factory(CustomerRepository)
    product_repo = providers.Factory(ProductRepository)



    # Khai báo DebtService trước
    debt_service = providers.Factory(DebtService, repository=debt_repo)
    
    



    # Tiêm debt_service vào OrderService
    order_service = providers.Factory(
        OrderService, 
        repository=order_repo, 
        debt_service=debt_service
    )
    report_service = providers.Factory(AccountReportService, repository=report_repo)
    ai_assistant_service = providers.Factory(
    AIAssistantService, 
    repository=ai_assistant_repo, 
    draft_repo=draft_repo
)
    ai_draft_order_service = providers.Factory(
    AIDraftOrderService,
    draft_repo=draft_repo,
    order_service=order_service,
    customer_repo=customer_repo, # Thêm cái này
    product_repo=product_repo # Kết nối trực tiếp với logic bán hàng
)