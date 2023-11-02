from abc import abstractmethod

class IRequisitionService():
    
    @abstractmethod
    def send_http_client(method: str, url: str):
        raise "Método 'send_http_client()' desse ser definido como 'IRequisitionService'"