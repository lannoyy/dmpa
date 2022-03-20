from alphabet import Alphabet
from transaction_table import TransactionTable
from transaction_table import FUNCTION_DICT


class FSM:
    def __init__(
        self,
        alphabet: Alphabet,
        start_state: str,
        final_states: str,
        transactions_table: TransactionTable,
    ):
        self.alphabet = alphabet
        self.current_state = start_state
        self.final_states = final_states
        self.transactions_table = transactions_table
        self.stack = []

    def process_str(self, str_to_process):
        for symbol in str_to_process:
            alphabet_symbols = self.alphabet.get_symbol_by_value(symbol)
            new_state = self.transactions_table.get_possible_transition(self.current_state, alphabet_symbols)
            function = self.transactions_table.get_function(self.current_state, new_state)
            if function != "None":
                FUNCTION_DICT[function](symbol)
            self.current_state = new_state
        return self.current_state in self.final_states["final_states"] and FUNCTION_DICT["FINISH_FUNCTION"]()

