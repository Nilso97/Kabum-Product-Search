import time
from core.logger.LoggerService import LoggerService


class UserService():

    def __init__(self) -> None:
        self.logger = LoggerService()

    def insert_values(self) -> dict:
        print('############## Kabum WebScraping Service (Black Friday) #################')
        insert_min_value = input(
            'Insira o valor minímo para iniciar a busca por produtos: R$')
        insert_max_value = input(
            'Insira o valor máximo para iniciar a busca por produtos: R$')
        print('#########################################################################')
        print('')
        self.logger.send_info_msg(
            'Processando as informações inseridas pelo usuário...')
        print('')
        time.sleep(2)
        input_values = self.check_correct_input(
            min_value=insert_min_value, max_value=insert_max_value)
        values = {
            'min': input_values[0],
            'max': input_values[1]
        }
        return values

    def check_correct_input(self, min_value, max_value) -> list:
        try:
            # TODO desenvolver inteligência para tratar valores com formatos inválidos
            if ',' in str(min_value) or ',' in str(max_value)\
                or str(min_value) == '' or str(max_value) == ''\
                    or int(min_value) == 0 or int(max_value) == 0 or '.' in str(min_value) or '.' in str(max_value):
                self.logger.send_alert_msg(
                    'Por favor, ao realizar a pesquisa: ')
                print('- Não utilizar valores com "," (vírgula)\n' +
                      '- Não utilizar valores com "." (ponto)\n' +
                      '- Não utilizar valores com casas decimais\n' +
                      '- Não inserir nenhum valor ou inserir valores nulos\n' +
                      '- etc...')
                print('')
                self.insert_values()
            insert_result = min_value, max_value
        except (Exception) as error:
            insert_result = str(error)
            self.logger.send_error_msg(
                f'Erro na função "check_correct_input()" ->  {insert_result}')
        finally:
            return insert_result

    def get_correct_values(self, min_value, max_value) -> list:
        """"""
        try:
            # TODO implementar/corrigir a lógica aqui de converter os valores inseridos
            min_value = int(min_value.replace('.', '')
                            ) if '.' in min_value or '.' in str(min_value) else int(min_value)
            max_value = int(max_value.replace('.', '')
                            ) if '.' in max_value or '.' in str(max_value) else int(max_value)
            correct_values = min_value, max_value
        except (Exception) as error:
            self.logger.send_error_msg(
                f'Erro na função "get_correct_values()" ->  {error}')
        return correct_values
