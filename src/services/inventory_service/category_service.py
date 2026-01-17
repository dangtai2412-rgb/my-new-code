from infrastructure.models.inventory.category_model import CategoryModel
from dependency_injector.wiring import inject, Provide

class CategoryService:
    @inject
    def __init__(self, category_repository):
        self.category_repository = category_repository

    def get_categories(self, owner_id):
        return self.category_repository.get_all(owner_id)

    def create_category(self, data, owner_id):
        new_category = CategoryModel(
            category_name=data['category_name'],
            description=data.get('description', ''),
            owner_id=owner_id
        )
        return self.category_repository.add(new_category)

    def delete_category(self, category_id):
        category = self.category_repository.get_by_id(category_id)
        if category:
            self.category_repository.delete(category)
            return True
        return False