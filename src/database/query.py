import typing
from src.models.Product import Product
from sqlalchemy import Row, text, null
from src.logs.logger.Logger import Logger
from src.database.DatabaseContext import db

logger = Logger()


def insert_products_data(products_list: list[dict]) -> None:
    for product in products_list:
        product_value_1 = f"'{product['Valor com desconto [Prime Ninja]']}'" if product["Valor com desconto [Prime Ninja]"] else null()
        product_value_2 = f"'{product['Valor [Black Friday]']}'" if product["Valor [Black Friday]"] else null()
        product_value_3 = f"'{product['Valor com desconto [Black Friday]']}'" if product["Valor com desconto [Black Friday]"] else null()
        if check_product_exists(product["Id"]):
            update_product_values(
                product=product,
                product_values=(
                    product_value_1,
                    product_value_2,
                    product_value_3
                )
            )
            continue
        db.session.execute(text(
            f"""INSERT INTO products 
            (
                id_produto, 
                produto, 
                valor_atual, 
                valor_prime_ninja, 
                valor_black_friday, 
                valor_black_friday_desconto
            ) VALUES (
                '{product["Id"]}',
                '{product["Produto"].replace("'", "")}',
                '{product["Valor atual"]}',
                {product_value_1},
                {product_value_2},
                {product_value_3}        
            );""")
        )
        db.session.commit()
    db.session.close()


def check_product_exists(product_id: int):
    product_exists = db.session.execute(
        text(f"SELECT id FROM products p WHERE p.id_produto={product_id}"))._allrows()
    return True if len(product_exists) > 0 else False


def update_product_values(product: dict, product_values: tuple) -> None:
    db.session.execute(text(f"""
        UPDATE products SET 
        valor_atual = '{product["Valor atual"]}',
        valor_prime_ninja = {product_values[0]},
        valor_black_friday = {product_values[1]},
        valor_black_friday_desconto = {product_values[2]}
        WHERE id_produto = {product["Id"]} and valor_atual > {product["Valor atual"]}
    """))
    db.session.commit()
    logger.message(f"Produto ID{product['Id']} atualizado com sucesso!")


def get_all_products() -> typing.Sequence[Row[tuple[Product]]]:
    products = db.session.execute(text("SELECT * FROM products"))._allrows()
    db.session.close()
    return products


def get_specific_product(product) -> list:
    products = db.session.execute(
        text(f"SELECT * FROM products p WHERE p.produto LIKE '%{product}%'"))._allrows()
    db.session.close()
    return products


def get_products_from_database(product: dict, products_list: list = []) -> list[dict]:
    for product_data in get_specific_product(product=product):
        products_list.append({
            "Produto": product_data.produto,
            "Valor Atual": product_data.valor_atual,
            "Valor Prime Ninja": product_data.valor_prime_ninja,
            "Valor Black Friday": product_data.valor_black_friday,
            "Valor Black Friday com desconto": product_data.valor_black_friday_desconto
        })
    return products_list
