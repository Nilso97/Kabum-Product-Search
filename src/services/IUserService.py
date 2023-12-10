from abc import ABC, abstractmethod


class IUserService(ABC):

    @abstractmethod
    def get_user_insert_search_values() -> dict:
        raise NotImplementedError('Método "get_user_insert_search_values" não implementado')

    @abstractmethod
    def get_default_incorrect_values_message():
        raise NotImplementedError('Método "get_default_incorrect_values_message" não implementado')
    
    @abstractmethod
    def check_user_inserted_values(
        min_value: int | str | float, 
        max_value: int | str | float
    ) -> tuple:
        raise NotImplementedError('Método "check_user_inserted_values" não implementado')
