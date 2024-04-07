from src.repositories.ProductRepository import ProductRepository


class ProductDataService:

    def __init__(self) -> None:
        self.__product_repository = ProductRepository()

    def get_products_data(self, product: dict) -> list:
        return self.__product_repository.get_products_from_database(product)

    def save_products_data(self, products_list: list) -> None:
        self.__product_repository.save_products_data(products_list)
