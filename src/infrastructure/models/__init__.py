from infrastructure.databases.base import Base

# 1. Access & Identity
from .access_and_identity.administrator_model import AdministratorModel
from .access_and_identity.business_owner_model import BusinessOwnerModel
from .access_and_identity.employee_model import EmployeeModel
from .access_and_identity.subscription_plan_model import SubscriptionPlanModel

# 2. Sale & Finance
from .sale_and_finance.customer_model import CustomerModel
from .sale_and_finance.order_model import OrderModel
from .sale_and_finance.order_detail_model import OrderDetailModel
from .sale_and_finance.debt_model import DebtModel
from .sale_and_finance.payment_model import PaymentModel
from .sale_and_finance.account_report_model import AccountReportModel

# 3. Inventory (Bổ sung phần thiếu)
from .inventory.unit_model import UnitModel
from .inventory.product_model import ProductModel
from .inventory.supplier_model import SupplierModel                
from .inventory.stock_import_model import StockImportModel         
from .inventory.stock_import_detail_model import StockImportDetailModel 

# 4. AI Core
from .ai_core.ai_assistant_model import AIAssistantModel
from .ai_core.ai_draft_order_model import AIDraftOrderModel

# 5. Utilities (Nếu có)
from .inventory.category_model import CategoryModel
from .inventory.inventory_check_model import InventoryCheckModel
from .inventory.inventory_check_detail_model import InventoryCheckDetailModel
from .sale_and_finance.return_order_model import ReturnOrderModel
from .sale_and_finance.return_order_detail_model import ReturnOrderDetailModel