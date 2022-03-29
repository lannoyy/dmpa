from alphabet import Alphabet
from transaction_table import TransactionTable
from transactions_funcs import FUNCTION_DICT, STACK_DICT
from error import ValidationError, AlphabetError



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
            if not alphabet_symbols:
                raise AlphabetError("Symbol not found in alphabet")
            new_state = self.transactions_table.get_possible_transition(self.current_state, alphabet_symbols)
            if not new_state:
                raise ValidationError("Bad string")
            functions = self.transactions_table.get_function(self.current_state, new_state)
            stack, symbol_for_stack = self.transactions_table.get_stack_with_symbol(self.current_state, new_state)
            self.current_state = new_state
            for stack_operation in stack:
                if symbol_for_stack != "current_symbol":
                    STACK_DICT[stack_operation](symbol_for_stack)
                else:
                    STACK_DICT[stack_operation](symbol)
            for function in functions:
                if function != "None":
                    FUNCTION_DICT[function]()
        return self.current_state in self.final_states["final_states"] and FUNCTION_DICT["FINISH_FUNCTION"]()

