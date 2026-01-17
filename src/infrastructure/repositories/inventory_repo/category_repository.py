from infrastructure.models.inventory.category_model import CategoryModel
from infrastructure.databases import session

class CategoryRepository:
    def get_all(self, owner_id):
        return session.query(CategoryModel).filter_by(owner_id=owner_id).all()

    def get_by_id(self, category_id):
        return session.query(CategoryModel).filter_by(category_id=category_id).first()

    def add(self, category):
        session.add(category)
        session.commit()
        return category

    def update(self):
        session.commit()

    def delete(self, category):
        session.delete(category)
        session.commit()