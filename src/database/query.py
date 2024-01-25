from sqlalchemy import text, null
from src.logs.logger.Logger import Logger
from src.database.DatabaseContext import db

logger = Logger()


def insert_products_data(products_list: list[dict], product_values: list = []) -> None:
    for product in products_list:
        for index, product_key in enumerate(list(product)):
            if index < 4:
                continue
            product_values.append(
                f"'{product[product_key]}'" if product[product_key] else null()
            )

        product_prices = (
            product_values[0],
            product_values[1],
            product_values[2]
        )
        product_exists_query = db.session.execute(text(
            f"SELECT id FROM products p WHERE p.id_produto={product['Id']}"
        ))
        if len(product_exists_query._allrows()) > 0:
            update_product_values(
                product=product,
                product_prices=product_prices
            )
            continue

        product_name = product["Produto"].replace("'", "")
        db.session.execute(text(
            f"""INSERT INTO products (
                id_produto, 
                produto, 
                valor_atual, 
                valor_prime_ninja, 
                valor_black_friday, 
                valor_black_friday_desconto
            ) VALUES (
                '{product["Id"]}',
                '{product_name}',
                '{product["Valor atual"]}',
                {product_prices[0]},
                {product_prices[1]},
                {product_prices[2]}       
            )""")
        )
        product_values = []

        db.session.commit()

    db.session.close()


def update_product_values(product: dict, product_prices: tuple) -> None:
    db.session.execute(text(
        f"""UPDATE products SET 
        valor_atual='{product["Valor atual"]}',
        valor_prime_ninja={product_prices[0]},
        valor_black_friday={product_prices[1]},
        valor_black_friday_desconto={product_prices[2]}
        WHERE id_produto={product["Id"]} and valor_atual > {product["Valor atual"]}
    """))
    db.session.commit()
    logger.message(f"Produto ID{product['Id']} atualizado com sucesso!")


def get_specific_product(product) -> list:
    products = db.session.execute(text(
        f"SELECT * FROM products p WHERE p.produto LIKE '%{product}%'"
    ))
    db.session.close()
    return products._allrows()


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
