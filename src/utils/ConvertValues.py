from datetime import datetime
from src.utils.IConvertValues import IConvertValues


class ConvertValues(IConvertValues):

    def __init__(self) -> None:
        super().__init__()

    def convert_values(self, value: str) -> int:
        if "." in value:
            converted_value = int(value.replace(".", ""))
        if "," in value:
            converted_value = int(value.replace(",", ""))
        else:
            converted_value = int(value)
        return converted_value
    
    def convert_datetime(self, format: str) -> str:
        formated_date = datetime.now().strftime(format)
        return formated_date
