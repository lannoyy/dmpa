import json


class TransactionTable:
    """
    Класс для работы с таблицей переходов
    """

    def __init__(
            self,
            transactions_table: str,
    ):
        with open(transactions_table) as file:
            self.transactions_table = json.loads(file.read())

    def _reverse_transitions(self, state) -> dict:
        """
        Метод для выдачи словаря вида символ: новое состояние
        """
        temp_dict = {}
        for key, value in self.transactions_table[state].items():
            split_value = value['symbol'].split(",")
            if split_value:
                for value_symbol in split_value:
                    temp_dict.update({value_symbol: key})
            else:
                temp_dict.update({value: key})
        return temp_dict

    def get_function(self, current_state: str, new_state: str):
        return self.transactions_table[current_state][new_state]['function']

    def get_possible_transition(self, state, symbols):
        temp_dict = self._reverse_transitions(state)
        for symbol in symbols:
            if symbol in temp_dict.keys():
                return temp_dict[symbol]
        return None

    def get_stack_with_symbol(self, current_state: str, new_state: str):
        return self.transactions_table[current_state][new_state]['action_with_stack'], \
               self.transactions_table[current_state][new_state]['symbol_for_stack'],
