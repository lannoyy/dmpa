from FSM import FSM
from alphabet import Alphabet
from transaction_table import TransactionTable
import json

def main(str):
    alphabet = Alphabet("alphabet.json")
    transaction_table = TransactionTable("transaction_table.json")
    with open("final_states.json") as file:
        final_states = json.loads(file.read())
    fsm = FSM(
        alphabet=alphabet,
        start_state="q0",
        final_states=final_states,
        transactions_table=transaction_table,
    )
    return (fsm.process_str(str))

if __name__ == "__main__":
    main("COST=(PRICE+TAXE)*0.98")


#Чтобы переделать на дмпа нужно вшить действия со стеком на уровне автомата
