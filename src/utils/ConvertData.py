from src.utils.IConvertData import IConvertData


class ConvertData(IConvertData):

    def __init__(self) -> None:
        super().__init__()

    def converted_values(self, value: str) -> int:
        if "." in value:
            converted_value = int(value.replace(".", ""))
        if "," in value:
            converted_value = int(value.replace(",", ""))
        else:
            converted_value = int(value)
        return converted_value
