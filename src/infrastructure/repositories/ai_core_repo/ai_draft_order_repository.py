from infrastructure.models.ai_core.ai_draft_order_model import AIDraftOrderModel
from domain.models.ai_draft_order import AIDraftOrder
from infrastructure.databases.mssql import session
import json
class AIDraftOrderRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, draft: AIDraftOrder):
        try:
            db_draft = AIDraftOrderModel(
                employee_id=draft.employee_id,
                ai_id=draft.ai_id,
                customer_id=draft.customer_id,
                recognized_content=draft.recognized_content,
                confirmation_status=draft.confirmation_status,
                source=draft.source
            )
            self.session.add(db_draft)
            self.session.commit()
            self.session.refresh(db_draft)
            return db_draft
        except Exception as e:
            self.session.rollback()
            raise e
        
    def create_draft(self, raw_text, extracted_json):
        """Lưu kết quả AI bóc tách được vào DB"""
        new_draft = AIDraftOrderModel(
            raw_text=raw_text,
            # Chuyển dict thành chuỗi JSON để lưu vào cột text/nvarchar
            extracted_json=json.dumps(extracted_json),
            status="Pending" # Trạng thái chờ xác nhận
        )
        try:
            self.session.add(new_draft)
            self.session.commit()
            self.session.refresh(new_draft)
            return new_draft
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, draft_id):
        return self.session.query(AIDraftOrderModel).filter_by(draft_id=draft_id).first()

    def update_status(self, draft_id, status):
        draft = self.get_by_id(draft_id)
        if draft:
            draft.status = status
            self.session.commit()
        return draft