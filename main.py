from src.KabumScrapService import KabumScrapService


def main():
    values = user_insert_value()
    scrap = KabumScrapService(min_value=values.get(
        'min'), max_value=values.get('max'))
    scrap.scrap_init()


def user_insert_value():
    ############## BUSCAR NOTEBOOKS "kabum.com.br" (Black Friday) #################
    insert_min_value = input(
        'Insira o valor minímo para iniciar a busca por produtos: R$')
    insert_max_value = input(
        'Insira o valor máximo para iniciar a busca por produtos: R$')
    ##############################################################################
    min_value = int(insert_min_value.replace('.', '')
                    ) if '.' in insert_min_value else int(insert_min_value)
    max_value = int(insert_max_value.replace('.', '')
                    ) if '.' in insert_max_value else int(insert_max_value)
    values = {
        'min': min_value,
        'max': max_value
    }
    return values


if __name__ == '__main__':
    main()
