from src.models.Product import Product
from sqlalchemy import text, null, update
from src.database.DatabaseContext import db


class ProductRepository:

    def get_product_prices(self, product: dict, max_rows: int = 4, product_prices: list = []) -> list:
        for row, key in enumerate(list(product)):
            if row < max_rows:
                continue

            product_prices.append(product[key] if product[key] else null())

    def save_products_data(self, products_list: list) -> None:
        for product_data in products_list:
            if self.check_products_exists(product_data):
                continue
                
            product_prices = self.get_product_prices(product_data)
            db.session.add(Product(
                kabum_product_id=product_data["Id"],
                product_name=product_data["Produto"].replace("'", ""),
                product_price=product_data["Valor atual"],
                product_prime_ninja_price=self.get_prime_ninja_price(product_prices),
                product_black_friday_price=self.get_black_friday_price(product_prices),
                product_black_friday_price_with_discount=self.get_black_friday_price_with_discount(product_prices)
            ))
            db.session.commit()

    def check_products_exists(self, product_data: dict) -> bool:
        product_prices = self.get_product_prices(product_data)
        exist_products = db.session.query(Product).where(Product.kabum_product_id == product_data["Id"]).all()
        if len(exist_products) > 0:
            self.update_product_prices(product_data, product_prices)
            return True

        return False

    def update_product_prices(self, product: dict, product_prices: list) -> None:
        db.session.execute(update(Product).where(
            (Product.kabum_product_id == product["Id"]) & (Product.product_price > product["Valor atual"])).values({
                Product.product_price: product["Valor atual"],
                Product.product_black_friday_price: self.get_black_friday_price(
                    product_prices
                ),
                Product.product_black_friday_price_with_discount: self.get_black_friday_price_with_discount(
                    product_prices
                ),
                Product.product_prime_ninja_price: self.get_prime_ninja_price(
                    product_prices
                )
            }))

        db.session.commit()

    def get_specific_product(self, product: str) -> list:
        query = db.session.execute(text(f"SELECT * FROM kabum_products p WHERE p.product_name ILIKE '%{product}%';"))

        return query._allrows()

    def get_products_from_database(self, product: dict, products_list: list = []) -> list:
        for product_data in self.get_specific_product(product):
            products_list.append({
                "Produto": product_data.product_name,
                "Valor Atual": product_data.product_price,
                "Valor Prime Ninja": product_data.product_prime_ninja_price,
                "Valor Black Friday": product_data.product_black_friday_price,
                "Valor Black Friday com desconto": product_data.product_black_friday_price_with_discount
            })

        return products_list

    def get_black_friday_price(self, product_prices: list) -> int: 
        return product_prices[0] if product_prices else null()
    
    def get_black_friday_price_with_discount(self, product_prices: list) -> int: 
        return product_prices[1] if product_prices and len(product_prices) > 1 else null()
    
    def get_prime_ninja_price(self, product_prices: list) -> int:
        return product_prices[2] if product_prices and len(product_prices) > 2 else null()