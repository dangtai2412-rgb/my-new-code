from dependency_injector import containers, providers
# Repositories
from infrastructure.repositories.sale_and_finance_repo.order_repository import OrderRepository
from infrastructure.repositories.sale_and_finance_repo.debt_repository import DebtRepository
from infrastructure.repositories.sale_and_finance_repo.customer_repository import CustomerRepository
from infrastructure.repositories.inventory_repo.product_repository import ProductRepository
from infrastructure.repositories.ai_core_repo.ai_draft_order_repository import AIDraftOrderRepository
from infrastructure.repositories.ai_core_repo.ai_assistant_repository import AIAssistantRepository

# Services
from services.sale_and_finance_service.order_service import OrderService
from services.sale_and_finance_service.debt_service import DebtService
from services.ai_sore_service.ai_assistant_service import AIAssistantService
from services.ai_sore_service.ai_draft_order_service import AIDraftOrderService

class Container(containers.DeclarativeContainer):
    # Khai báo Repository
    order_repo = providers.Factory(OrderRepository)
    debt_repo = providers.Factory(DebtRepository)
    customer_repo = providers.Factory(CustomerRepository)
    product_repo = providers.Factory(ProductRepository)
    draft_repo = providers.Factory(AIDraftOrderRepository)
    ai_assistant_repo = providers.Factory(AIAssistantRepository)

    # Khai báo Service
    debt_service = providers.Factory(DebtService, repository=debt_repo)
    
    order_service = providers.Factory(
        OrderService, 
        repository=order_repo, 
        debt_service=debt_service
    )

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