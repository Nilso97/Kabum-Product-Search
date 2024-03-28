from src.models.Product import Product
from sqlalchemy import text, null, update
from src.database.DatabaseContext import db


class ProductRepository:

    def get_product_prices(self, product: dict, max_rows: int = 4, product_prices: list = []) -> list:
        for row, key in enumerate(list(product)):
            if row < max_rows:
                continue

            product_prices.append(f"'{product[key]}'" if product[key] else null())

    def insert_products_data(self, products_list: list[dict]) -> None:
        for product_data in products_list:
            self.check_exists_products(product_data)
            product_prices = self.get_product_prices(product_data)
            db.session.add(Product(
                id_produto=product_data["Id"],
                produto=product_data["Produto"].replace("'", ""),
                valor_atual=product_data["Valor atual"],
                valor_black_friday=product_prices[0] if product_prices else null(),
                valor_black_friday_desconto=product_prices[1] if product_prices and len(product_prices) > 1 else null(),
                valor_prime_ninja=product_prices[2] if product_prices and len(product_prices) > 2 else null()
            ))
            db.session.commit()

    def check_exists_products(self, product_data: dict):
        product_prices = self.get_product_prices(product_data)
        exist_products = db.session.query(Product).where(Product.id_produto == product_data["Id"]).all()
        if len(exist_products) > 0:
            self.update_product_prices(product_data, product_prices)

    def update_product_prices(self, product: dict, product_prices: list) -> None:
        update(Product).where(
            Product.id_produto == product["Id"] and Product.valor_atual > product["Valor atual"]).values({
            Product.valor_atual: product["Valor atual"],
            Product.valor_black_friday: product_prices[0] if product_prices else null(),
            Product.valor_black_friday_desconto: product_prices[1] if product_prices and len(product_prices) > 1 else null(),
            Product.valor_prime_ninja: product_prices[2] if product_prices and len(product_prices) > 2 else null(),
        })

    def get_specific_product(self, product: str) -> list:
        return db.session.execute(text(f"SELECT * FROM products p WHERE p.produto LIKE '%{product}%'"))._allrows()

    def get_products_from_database(self, product: dict, products_list: list = []) -> list[dict]:
        for product_data in self.get_specific_product(product):
            products_list.append({
                "Produto": product_data.produto,
                "Valor Atual": product_data.valor_atual,
                "Valor Prime Ninja": product_data.valor_prime_ninja,
                "Valor Black Friday": product_data.valor_black_friday,
                "Valor Black Friday com desconto": product_data.valor_black_friday_desconto
            })

        return products_list
