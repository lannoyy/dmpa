import re

VARIABLES_STORE = []
index = 1

OPERATIONAL_STACK = []
VARIABLES_STACK = []
CYCLE_BREAK_STACK = []


STACK_DICT = {
    "PUSH_TO_VARIABLE_STACK": VARIABLES_STACK.append,
    "PUSH_TO_OPERATIONAL_STACK": OPERATIONAL_STACK.append,
    "PUSH_TO_CYCLE_BREAK_STACK": CYCLE_BREAK_STACK.append,
}

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

def make_operation(operation=None):
    global index
    if not operation:
        operation = OPERATIONAL_STACK.pop()
    if operation == ")":
        return
    right = VARIABLES_STORE.pop()
    left = VARIABLES_STORE.pop()
    value = ""
    if operation == "+":
        value = f"{right};STORE ${index};LOAD {left};ADD ${index}"
    elif operation == "*":
        value = f"{right};STORE ${index};LOAD {left};MPY ${index}"
    elif operation == "=":
        value = f"LOAD {right};STORE {left}"
    VARIABLES_STORE.append(value)
    index += 1


def add_variable():
    if not VARIABLES_STACK:
        return
    temp_name = "".join(VARIABLES_STACK)
    if is_number(temp_name):
        temp_name = f"={temp_name}"
    VARIABLES_STORE.append(temp_name)
    VARIABLES_STACK.clear()

def bracket_operation():
    operation = OPERATIONAL_STACK.pop()
    if operation == ")":
        CYCLE_BREAK_STACK.pop()
        while operation != "(":
            make_operation(operation)
            operation = OPERATIONAL_STACK.pop()




def optimization():
    code_for_optimization = VARIABLES_STORE[0]
    print(code_for_optimization)
    code_for_optimization = first_rule(code_for_optimization)
    code_for_optimization = second_rule(code_for_optimization)
    code_for_optimization = third_rule(code_for_optimization)
    code_for_optimization = fourth_rule(code_for_optimization)

def finish_function():
    add_variable()
    while OPERATIONAL_STACK:
        make_operation()
        if not OPERATIONAL_STACK:
            break
    optimization()
    return not CYCLE_BREAK_STACK


FUNCTION_DICT = {
    "ADD_VARIABLE": add_variable,
    "FINISH_FUNCTION": finish_function,
    "BRACKET_OPERATION": bracket_operation
}