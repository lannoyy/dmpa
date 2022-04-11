import re

CYCLE_BREAK_STORE = []
OPERATION_STORE = []
VARIABLE_NAME_STORE = []
VARIABLES_STORE = []
index = 0

def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def first_rule(code_for_optimization):
    ''' First step in code optimization, for more info look for table 2.4 in methodical instructions '''
    first_pattern = "LOAD [=$0-9.A-Za-z+-]+;ADD [=$0-9.A-Za-z+-]+;"
    first_rule = re.findall(first_pattern, code_for_optimization)
    resultCodeArray = VARIABLES_STORE[0].split(';')
    if first_rule:
        for i in first_rule:
            item = i.split(';')[1]
            if resultCodeArray.count(item) < 2:
                alfa = i.split(";")[0].split(" ")[1]
                beta = i.split(";")[1].split(" ")[1]
                code_for_optimization = code_for_optimization.replace(i, f"LOAD {beta};ADD {alfa};")
    print(f"{code_for_optimization} After 1") # для наглядности
    return code_for_optimization

def second_rule(code_for_optimization):
    ''' Second step in code optimization, for more info look for table 2.4 in methodical instructions '''
    second_pattern = "LOAD [=$0-9.A-Za-z+-]+;MPY [=$0-9.A-Za-z+-]+;"
    second_rule = re.findall(second_pattern, code_for_optimization)
    resultCodeArray = VARIABLES_STORE[0].split(';')
    if second_rule:
        for i in second_rule:
            item = i.split(';')[1]
            if resultCodeArray.count(item) < 2:
                alfa = i.split(";")[0].split(" ")[1]
                beta = i.split(";")[1].split(" ")[1]
                code_for_optimization = code_for_optimization.replace(i, f"LOAD {beta};MPY {alfa};")
    print(f"{code_for_optimization} After 2") # для наглядности
    return code_for_optimization

def third_rule(code_for_optimization):
    ''' Third step in code optimization, for more info look for table 2.4 in methodical instructions '''
    third_pattern = "STORE [=$0-9.A-Za-z+-]+;LOAD [=$0-9.A-Za-z+-]+;"
    third_rule = re.findall(third_pattern, code_for_optimization)
    item_pattern = "[$.0-9]+"
    resultCodeArray = VARIABLES_STORE[0].split(';')
    if third_rule:
        for i in third_rule:
            if len(re.findall(item_pattern, i)) != 2:
                continue
            if len(list(filter(lambda item: item.split(' ')[1] == i.split(';')[0].split(' ')[1], resultCodeArray))) < 3 \
                    and re.findall(item_pattern, i)[0] == re.findall(item_pattern, i)[1]:
                code_for_optimization = code_for_optimization.replace(i, '')
    print(f"{code_for_optimization} After 3") # для наглядности
    return code_for_optimization

def fourth_rule(code_for_optimization):
    ''' Fourth step in code optimization, for more info look for table 2.4 in methodical instructions '''
    fourth_pattern = "LOAD [=$0-9.A-Za-z+-]+;STORE [=$0-9.A-Za-z+-]+;LOAD"
    fourth_rule = re.findall(fourth_pattern, code_for_optimization)
    another_pattern = "[A-Z]+ [=$0-9.A-Za-z+-]+;"
    while fourth_rule:
        if fourth_rule:
            for item in fourth_rule:
                temp = item.split(';')
                if temp[0].split(' ')[1] != temp[1].split(' ')[1]:
                    alfa = temp[0].split(' ')[1]
                    beta = temp[1].split(' ')[1]
                    code_for_optimization = code_for_optimization.replace(temp[0] + ';', '', 1)
                    code_for_optimization = code_for_optimization.replace(temp[1] + ';', '', 1)
                    temp_code = code_for_optimization.split(';')
                    another_rule = re.findall(another_pattern, code_for_optimization)
                    index_for_while = 0
                    while another_rule and temp_code[index_for_while] != f"STORE {beta}":
                        if temp_code[index_for_while].split(' ')[1] == beta:
                            code_for_optimization = code_for_optimization.replace(beta, alfa, 1)
                            temp_code[index_for_while] = temp_code[index_for_while].split(' ')[0] + ' ' + alfa
                        index_for_while += 1
                        if index_for_while + 1 >= len(temp_code):
                            break
                        another_rule = re.findall(another_pattern, code_for_optimization)
        fourth_rule = re.findall(fourth_pattern, code_for_optimization)
    return code_for_optimization

def make_operation(operation, move=None):
    if not operation:
        operation = OPERATION_STORE.pop()
    if operation == "(" or operation == ")":
        return
    if move:
        right = VARIABLES_STORE.pop(move)
        left = VARIABLES_STORE.pop(move)
    else:
        right = VARIABLES_STORE.pop()
        left = VARIABLES_STORE.pop()
    # print(f"right {right}, operation {operation}, left {left}")
    if operation == "+":
        if right.rfind("$") != -1 and left.rfind("$") != -1:
            index = max(int(right[right.rfind("$") + 1]), int(left[left.rfind("$") + 1])) + 1
        elif right.rfind("$") != -1:
            index = int(right[right.rfind("$") + 1]) + 1
        elif left.rfind("$") != -1:
            index = int(left[left.rfind("$") + 1]) + 1
        else:
            index = 1
        value = f"{right};STORE ${index};LOAD {left};ADD ${index}"
    elif operation == "*":
        if right.rfind("$") != -1 and left.rfind("$") != -1:
            index = max(int(right[right.rfind("$") + 1]), int(left[left.rfind("$") + 1])) + 1
        elif right.rfind("$") != -1:
            index = int(right[right.rfind("$") + 1]) + 1
        elif left.rfind("$") != -1:
            index = int(left[left.rfind("$") + 1]) + 1
        else:
            index = 1
        value = f"{right};STORE ${index};LOAD {left};MPY ${index}"
    elif operation == "=":
        value = f"LOAD {right};STORE {left}"
    if move:
        VARIABLE_NAME_STORE.insert(move, value)
    else:
        VARIABLE_NAME_STORE.append(value)
    # print(f"VARIABLE_NAME_STORE = {VARIABLE_NAME_STORE}\n")
    add_variable()


def add_operation(current_symbol):
    add_variable()
    if current_symbol == " ":
        return
    elif current_symbol == "(":
        CYCLE_BREAK_STORE.append(current_symbol)
    elif current_symbol == ")":
        operation = OPERATION_STORE.pop()
        CYCLE_BREAK_STORE.pop()
        while operation != "(":
            make_operation(operation)
            operation = OPERATION_STORE.pop()
    elif current_symbol == "+" and OPERATION_STORE[-1] == "*":
        make_operation(OPERATION_STORE.pop())
    if (current_symbol != ')'):
        OPERATION_STORE.append(current_symbol)


def collect_variable_name(current_symbol):
    VARIABLE_NAME_STORE.append(current_symbol)


def add_variable():
    if not VARIABLE_NAME_STORE:
        return
    temp_name = "".join(VARIABLE_NAME_STORE)
    if is_number(temp_name):
        temp_name = f"={temp_name}"
    VARIABLES_STORE.append(temp_name)

    VARIABLE_NAME_STORE.clear()


def optimization():
    code_for_optimization = VARIABLES_STORE[0]
    print(f"Code before optimization\n{code_for_optimization}\n") # для наглядности
    code_for_optimization = first_rule(code_for_optimization)
    code_for_optimization = second_rule(code_for_optimization)
    code_for_optimization = third_rule(code_for_optimization)
    code_for_optimization = fourth_rule(code_for_optimization)
    print(f"Code after optimization\n{code_for_optimization}") # для наглядности

def finish_function():
    add_variable()
    operation = OPERATION_STORE.pop()
    while operation:
        if '*' in OPERATION_STORE:
            move = OPERATION_STORE.index('*')
            make_operation(OPERATION_STORE.pop(move), move=move)
            OPERATION_STORE.append(operation)
        else:
            make_operation(operation)
        if not OPERATION_STORE:
            break
        operation = OPERATION_STORE.pop()
    optimization()
    return not CYCLE_BREAK_STORE



FUNCTION_DICT = {
    "ADD_OPERATION": add_operation,
    "COLLECT_VARIABLE_NAME": collect_variable_name,
    "ADD_VARIABLE": add_variable,
    "FINISH_FUNCTION": finish_function
}