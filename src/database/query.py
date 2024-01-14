import typing
from src.models.Product import Product
from src.logs.logger.Logger import Logger
from sqlalchemy import Row, select, update
from src.database.DatabaseContext import db

logger = Logger()

def insert_products_data(products_list: list[dict]) -> None:
    for product in products_list:
        product_exists = check_product_exists(product["Id"])
        if product_exists:
            update_product_values(product=product)
            continue
        product_object = make_products_object(product=product)
        db.session.add(instance=product_object)
        db.session.commit()
    db.session.close()

def check_product_exists(product_id: int):
    product_exists = db.session.execute(select(Product).where(Product.id_produto == product_id)).all()
    return True if len(product_exists) > 0 else False

def update_product_values(product: dict) -> None:
    db.session.execute(
        update(Product)
        .where(
            Product.id_produto == product["Id"]
            and
            Product.valor_atual <= product["Valor atual"])
        .values({
            Product.valor_atual: product["Valor atual"],
            Product.valor_black_friday: product["Valor com desconto [Prime Ninja]"],
            Product.valor_black_friday: product["Valor [Black Friday]"],
            Product.valor_black_friday_desconto: product["Valor com desconto [Black Friday]"]
        })
    )
    db.session.commit()
    logger.message(f"Produto ID{product['Id']} atualizado com sucesso!")

def get_all_products() -> typing.Sequence[Row[tuple[Product]]]:
    products = db.session.execute(select(Product)).all()
    db.session.close()
    return products

def get_specific_product(product) -> list:
    products = Product.query.filter(Product.produto.contains(product)).order_by(Product.valor_atual).all()
    db.session.close()
    return products

def make_products_object(product: dict) -> Product:
    product_object = Product(
        produto=product["Produto"],
        id_produto=product["Id"],
        descricao=product["Descricao"],
        valor_atual=product["Valor atual"],
        valor_prime_ninja=product["Valor com desconto [Prime Ninja]"],
        valor_black_friday=product["Valor [Black Friday]"],
        valor_black_friday_desconto=product["Valor com desconto [Black Friday]"]
    )
    return product_object

def get_products_from_database(product: dict, products_list: list = []) -> list[dict]:
    for product_data in get_specific_product(product=product):
        products_list.append({
            "Produto": product_data.produto,
            "Descrição": product_data.descricao,
            "Valor Atual": product_data.valor_atual,
            "Valor [Prime Ninja]": product_data.valor_prime_ninja,
            "Valor [Black Friday]": product_data.valor_black_friday,
            "Valor [Black Friday] c/ desconto": product_data.valor_black_friday_desconto
        })
    return products_list