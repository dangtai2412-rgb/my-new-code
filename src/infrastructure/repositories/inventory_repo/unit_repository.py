from infrastructure.models.inventory.unit_model import UnitModel
from infrastructure.databases.mssql import session

class UnitRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, product_id, name, rate, is_base):
        db_unit = UnitModel(product_id=product_id, unit_name=name, conversion_rate=rate, is_base_unit=is_base)
        self.session.add(db_unit)
        self.session.commit()
        self.session.refresh(db_unit)
        return db_unit

    def get_by_product(self, product_id):
        return self.session.query(UnitModel).filter_by(product_id=product_id).all()
    def delete(self, unit_id):
        """Xóa đơn vị tính"""
        try:
            unit = self.session.query(UnitModel).filter_by(unit_id=unit_id).first()
            if unit:
                self.session.delete(unit)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e
        # Đoạn code bạn đã có:
