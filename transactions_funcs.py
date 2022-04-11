import re

VARIABLES_STORE = []

OPERATIONAL_STACK = []
VARIABLES_STACK = []
CYCLE_BREAK_STACK = []


def add_operation(current_symbol):
    if current_symbol == "(":
        CYCLE_BREAK_STACK.append(current_symbol)
    add_variable()
    if current_symbol == "+":
        if len(OPERATIONAL_STACK) >= 2:
            if OPERATIONAL_STACK[-1] == "*":
                make_operation(OPERATIONAL_STACK.pop())
    OPERATIONAL_STACK.append(current_symbol)

STACK_DICT = {
    "PUSH_TO_VARIABLE_STACK": VARIABLES_STACK.append,
    "PUSH_TO_OPERATIONAL_STACK": add_operation,
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

def make_operation(operation=None, move=None):
    if not operation:
        operation = OPERATIONAL_STACK.pop()
    if operation == "(" or operation == ")":
        return
    if move:
        left = VARIABLES_STORE.pop(move)
        right = VARIABLES_STORE.pop(move)
    else:
        right = VARIABLES_STORE.pop()
        left = VARIABLES_STORE.pop()
    print(f"right {right}, operation {operation}, left {left}")
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
        VARIABLES_STORE.insert(move, value)
    else:
        VARIABLES_STORE.append(value)
    add_variable()


def add_variable():
    if not VARIABLES_STACK:
        return
    temp_name = "".join(VARIABLES_STACK)
    if is_number(temp_name):
        temp_name = f"={temp_name}"
    VARIABLES_STORE.append(temp_name)
    VARIABLES_STACK.clear()

def bracket_operation():
    CYCLE_BREAK_STACK.pop()
    operation = ""
    while operation != "(":
        last_bracket = max(loc for loc, val in enumerate(OPERATIONAL_STACK) if val == "(")
        if '*' in OPERATIONAL_STACK[last_bracket:]:
            move = max(loc for loc, val in enumerate(OPERATIONAL_STACK) if val == "*")
            operation = OPERATIONAL_STACK.pop(move)
            make_operation(operation, move-OPERATIONAL_STACK.count('('))
        else:
            operation = OPERATIONAL_STACK.pop()
            make_operation(operation)




def optimization():
    code_for_optimization = VARIABLES_STORE[0]
    print(code_for_optimization, "Before optimization")
    code_for_optimization = first_rule(code_for_optimization)
    code_for_optimization = second_rule(code_for_optimization)
    code_for_optimization = third_rule(code_for_optimization)
    code_for_optimization = fourth_rule(code_for_optimization)
    print(code_for_optimization, "After optimization")

def finish_function():
    add_variable()
    operation = OPERATIONAL_STACK.pop()
    while operation:
        if '*' in OPERATIONAL_STACK:
            move = OPERATIONAL_STACK.index('*')
            make_operation(OPERATIONAL_STACK.pop(move), move=move)
            OPERATIONAL_STACK.append(operation)
        else:
            make_operation(operation)
        if not OPERATIONAL_STACK:
            break
        operation = OPERATIONAL_STACK.pop()
    optimization()
    return not CYCLE_BREAK_STACK


FUNCTION_DICT = {
    "ADD_VARIABLE": add_variable,
    "FINISH_FUNCTION": finish_function,
    "BRACKET_OPERATION": bracket_operation
}