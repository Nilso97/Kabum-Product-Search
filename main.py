from src.KabumScrapService import KabumScrapService


def main():
    search_price = user_insert_value()
    scrap = KabumScrapService(search_price)
    scrap.scrap_init()


def user_insert_value():
    ############## BUSCAR NOTEBOOKS "kabum.com.br" (Black Friday) #################
    insert_value = input('Insira uma valor para iniciar a busca por produtos: R$')
    ##############################################################################
    return int(insert_value.replace('.', '')) if '.' in insert_value else int(insert_value)


if __name__ == '__main__':
    main()
