import time
from core.logger.LoggerService import LoggerService


class UserService():

    def __init__(self) -> None:
        self.logger = LoggerService()
        self.success = False
        self.execution = 1
        self.inserted_values = None

    def insert_values(self) -> dict:
        """"""
        try:
            print('############## Kabum WebScraping Service (Black Friday) #################')
            insert_min_value = input(
                'Insira o valor minímo para iniciar a busca por produtos: R$')
            insert_max_value = input(
                'Insira o valor máximo para iniciar a busca por produtos: R$')
            print('#########################################################################')
            print('')
            self.logger.send_info_msg('Processando as informações inseridas pelo usuário...')
            print('')
            time.sleep(1)
            correct_values = self.check_correct_values(min_value=insert_min_value, max_value=insert_max_value)
            if self.success is True and self.execution == 2:
                self.inserted_values = {
                    'min': correct_values[0],
                    'max': correct_values[1]
                }
                return
        except (Exception) as _:
            self.default_alert_message()
            self.insert_values()
        finally:
            return self.inserted_values

    def default_alert_message(self):
        """"""
        self.logger.send_alert_msg('Por favor, ao realizar a pesquisa: ')
        print('- Não utilizar valores com "," (vírgula)\n' +
              '- Não utilizar valores com "." (ponto)\n' +
              '- Não utilizar valores com casas decimais\n' +
              '- Não inserir nenhum valor ou inserir valores nulos\n' +
              '- etc...')
        print('')

    def check_correct_values(self, min_value, max_value) -> tuple:
        """"""
        try:
            values = min_value, max_value
            if ',' in str(min_value) or ',' in str(max_value):
                self.default_alert_message()
                self.insert_values()
            elif str(min_value) == '' or str(max_value) == '':
                self.default_alert_message()
                self.insert_values()
            elif int(min_value) == 0 or int(max_value.replace('.', '')) == 0:
                self.default_alert_message()
                self.insert_values()
            elif '.' in str(min_value) or '.' in str(max_value):
                self.default_alert_message()
                self.insert_values()
        except (Exception) as _:
            self.default_alert_message()
            self.insert_values()
        finally:
            self.success = True
            self.execution += 1
            return values
