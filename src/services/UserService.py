import time
from logs.logger.Logger import Logger
from src.services.IUserService import IUserService


class UserService(IUserService):

    def __init__(self) -> None:
        self.logger = Logger()
        self.execution = 1
        self.inserted_values = None

    def get_user_insert_search_values(self) -> dict:
        """"""
        try:
            print('############## KABUM Consulta de preços (Black Friday) #################\n')
            insert_min_value = input(
                'Insira o valor minímo para iniciar a busca por produtos: R$')
            insert_max_value = input(
                'Insira o valor máximo para iniciar a busca por produtos: R$')
            print('#########################################################################\n')
            self.logger.information('Processando as informações inseridas pelo usuário\n\nAguarde...\n')
            time.sleep(1)
            correct_values = self.check_user_inserted_values(
                min_value=insert_min_value, max_value=insert_max_value)
            if self.correct_values is True and self.execution == 2:
                self.inserted_values = {
                    'min': correct_values[0],
                    'max': correct_values[1]
                }
                return
        except (Exception) as _:
            self.get_default_incorrect_values_message()
            self.check_user_inserted_values()
        finally:
            return self.inserted_values

    def get_default_incorrect_values_message(self):
        """"""
        self.logger.alert('Por favor, ao realizar a pesquisa: ')
        print('- Não utilizar valores com "," (vírgula)\n' +
              '- Não utilizar valores com "." (ponto)\n' +
              '- Não utilizar valores com casas decimais\n' +
              '- Não inserir inserir valores nulos\n' +
              '- etc...\n')

    def check_user_inserted_values(
        self, 
        min_value: int | str | float, 
        max_value: int | str | float
    ) -> tuple:
        """"""
        self.correct_values = False
        try:
            inserted_values = min_value, max_value
            if ',' in str(min_value) or ',' in str(max_value):
                self.get_default_incorrect_values_message()
                self.get_user_insert_search_values()
            elif str(min_value) == '' or str(max_value) == '':
                self.get_default_incorrect_values_message()
                self.get_user_insert_search_values()
            elif int(min_value) == 0 or int(max_value.replace('.', '')) == 0:
                self.get_default_incorrect_values_message()
                self.get_user_insert_search_values()
            elif '.' in str(min_value) or '.' in str(max_value):
                self.get_default_incorrect_values_message()
                self.get_user_insert_search_values()
        except (Exception) as _:
            self.get_default_incorrect_values_message()
            self.get_user_insert_search_values()
        finally:
            self.correct_values = True
            self.execution += 1
            return inserted_values
