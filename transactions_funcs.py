import re

CYCLE_BREAK_STORE = []
OPERATION_STORE = []
VARIABLE_NAME_STORE = []
VARIABLES_STORE = []
index = 1

def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def first_rule(code_for_optimization):
    ''' First step in code optimization, for more info look for table 2.4 in methodical instructions '''
    first_pattern = "LOAD [$0-9.A-Za-z]+;ADD [$0-9.A-Za-z]+;"
    first_rule = re.findall(first_pattern, code_for_optimization)
    resultCodeArray = VARIABLES_STORE[0].split(';')

    if first_rule:
        for i in first_rule:
            item = i.split(';')[1]
            if resultCodeArray.count(item) < 2:
                alfa = i.split(";")[0].split(" ")[1]
                beta = i.split(";")[1].split(" ")[1]
                code_for_optimization = code_for_optimization.replace(i, f"LOAD {beta};ADD {alfa};")
    return code_for_optimization

def second_rule(code_for_optimization):
    ''' Second step in code optimization, for more info look for table 2.4 in methodical instructions '''
    second_pattern = "LOAD [$0-9.A-Za-z]+;MPY [$0-9.A-Za-z]+;"
    second_rule = re.findall(second_pattern, code_for_optimization)
    resultCodeArray = VARIABLES_STORE[0].split(';')
    if second_rule:
        for i in second_rule:
            item = i.split(';')[1]
            if resultCodeArray.count(item) < 2:
                alfa = i.split(";")[0].split(" ")[1]
                beta = i.split(";")[1].split(" ")[1]
                code_for_optimization = code_for_optimization.replace(item, f"LOAD {beta};MRY {alfa};")
    return code_for_optimization

def third_rule(code_for_optimization):
    ''' Third step in code optimization, for more info look for table 2.4 in methodical instructions '''
    third_pattern = "STORE [$0-9.A-Za-z]+;LOAD [$0-9.A-Za-z]+;"
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
    return code_for_optimization

def fourth_rule(code_for_optimization):
    ''' Fourth step in code optimization, for more info look for table 2.4 in methodical instructions '''
    fourth_pattern = "LOAD [=$0-9.A-Za-z]+;STORE [=$0-9.A-Za-z]+;LOAD"
    fourth_rule = re.findall(fourth_pattern, code_for_optimization)
    another_pattern = "LOAD [=$0-9.a-z]+;STORE "
    while fourth_rule:
        if fourth_rule:
            for item in fourth_rule:
                temp = item.split(';')
                if temp[0].split(' ')[1] != temp[1].split(' ')[1]:
                    alfa = temp[0].split(' ')[1]
                    beta = temp[1].split(' ')[1]
                    code_for_optimization = code_for_optimization.replace(temp[0] + ';', '').replace(temp[1] + ';', '').replace(beta, alfa)
        fourth_rule = re.findall(another_pattern, code_for_optimization)
    return code_for_optimization

def make_operation(operation):
    global index
    right = VARIABLES_STORE.pop()
    left = VARIABLES_STORE.pop()
    if operation == "+":
        value = f"{right};STORE ${index};LOAD {left};ADD ${index}"
    elif operation == "*":
        value = f"{right};STORE ${index};LOAD {left};MPY ${index}"
    elif operation == "=":
        value = f"LOAD {right};STORE {left}"
    VARIABLE_NAME_STORE.append(value)
    add_variable()
    index += 1


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
    code_for_optimization = first_rule(code_for_optimization)
    code_for_optimization = second_rule(code_for_optimization)
    code_for_optimization = third_rule(code_for_optimization)
    code_for_optimization = fourth_rule(code_for_optimization)
    print(code_for_optimization)

def finish_function():

    add_variable()
    operation = OPERATION_STORE.pop()
    while operation:
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