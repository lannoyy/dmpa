import json


class Alphabet:
    """
    Класс для работы с алфавитом
    """

    def __init__(self, alphabet: str):
        with open(alphabet) as file:
            self.alphabet = json.loads(file.read())

    def get_symbol_by_value(self, str_value):
        symbols = []
        for symbol, value in self.alphabet.items():
            if str_value in value["symbols"]:
                symbols.append(symbol)
        return symbols
