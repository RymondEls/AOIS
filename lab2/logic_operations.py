from itertools import product

OPERATORS = {
    '!': {'prec': 4, 'assoc': 'right', 'args': 1},
    '&': {'prec': 3, 'assoc': 'left', 'args': 2},
    '|': {'prec': 2, 'assoc': 'left', 'args': 2},
    '>': {'prec': 1, 'assoc': 'right', 'args': 2},
    '~': {'prec': 1, 'assoc': 'left', 'args': 2}
}

def function_spellcheck(expression):
    variables = []
    brackets_balance = 0
    for char in expression:
        if 'a' <= char <= 'z':
            if char not in variables:
                variables.append(char)
        elif char == '(':
            brackets_balance += 1
        elif char == ')':
            brackets_balance -= 1
            if brackets_balance < 0:
                return variables, False
        elif char in OPERATORS or char == ' ':
            pass
        else:
            return variables, False
    if brackets_balance != 0:
        return variables, False
    return variables, True

def shunting_yard(expression):
    output = []
    operator_stack = []
    
    i = 0
    while i < len(expression):
        token = expression[i]
        
        if token == ' ':
            i += 1
            continue
        
        if 'a' <= token <= 'z':
            output.append(token)
            i += 1
        elif token in OPERATORS:
            while (operator_stack and operator_stack[-1] != '(' and
                   ((OPERATORS[operator_stack[-1]]['prec'] > OPERATORS[token]['prec']) or
                    (OPERATORS[operator_stack[-1]]['prec'] == OPERATORS[token]['prec'] and
                     OPERATORS[token]['assoc'] == 'left'))):
                output.append(operator_stack.pop())
            operator_stack.append(token)
            i += 1
        elif token == '(':
            operator_stack.append(token)
            i += 1
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()
            i += 1
    
    while operator_stack:
        output.append(operator_stack.pop())
    
    return output

def evaluate_rpn(rpn, variables, values):
    stack = []
    steps = []
    seen_expr = set()

    for token in rpn:
        if token in variables:
            stack.append((token, values[token]))
        elif token in OPERATORS:
            if OPERATORS[token]['args'] == 1:
                (a_str, a_val) = stack.pop()
                expr = f"!{a_str}"
                result = int(not a_val)
            else:
                (b_str, b_val) = stack.pop()
                (a_str, a_val) = stack.pop()

                if token == '&':
                    expr = f"({a_str}&{b_str})"
                    result = int(a_val and b_val)
                elif token == '|':
                    expr = f"({a_str}|{b_str})"
                    result = int(a_val or b_val)
                elif token == '>':
                    expr = f"({a_str}>{b_str})"
                    result = int((not a_val) or b_val)
                elif token == '~':
                    expr = f"({a_str}~{b_str})"
                    result = int(a_val == b_val)

            if expr not in seen_expr:
                steps.append((expr, result))
                seen_expr.add(expr)
            stack.append((expr, result))

    final_result = stack[-1][1]
    return final_result, steps

def build_truth_table(expression, variables):
    rpn = shunting_yard(expression)
    truth_table = []
    intermediate_names = []
    rows = []

    for values in product([False, True], repeat=len(variables)):
        value_dict = dict(zip(variables, values))
        result, steps = evaluate_rpn(rpn, variables, value_dict)
        step_dict = {name: val for name, val in steps}
        if not intermediate_names:
            intermediate_names = [name for name, _ in steps]
        row = [int(value_dict[v]) for v in variables] + [step_dict[name] for name in intermediate_names] + [result]
        rows.append(row)

    header = variables + intermediate_names + [expression]
    truth_table.append(header)
    truth_table.extend(rows)
    return truth_table

def print_truth_table(table):
    if not table:
        print("Пустая таблица")
        return

    col_widths = [max(len(str(row[i])) for row in table) for i in range(len(table[0]))]
    separator = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+"

    def print_row(row):
        print("| " + " | ".join(f"{str(val):^{col_widths[i]}}" for i, val in enumerate(row)) + " |")

    print(separator)
    print_row(table[0])
    print(separator)
    for row in table[1:]:
        print_row(row)
    print(separator)

def get_normal_forms(table, variables):
    sdnf = []
    sknf = []
    idx_sdnf = []
    idx_sknf = []

    for i, row in enumerate(table[1:]):
        values = row[:len(variables)]
        result = row[-1]
        terms = []
        if result == 1:
            idx_sdnf.append(i)
            for var, val in zip(variables, values):
                terms.append(f"{'' if val else '¬'}{var}")
            sdnf.append("(" + "∧".join(terms) + ")")
        else:
            idx_sknf.append(i)
            for var, val in zip(variables, values):
                terms.append(f"{var if val else '¬' + var}")
            sknf.append("(" + "∨".join(terms) + ")")

    return " ∨ ".join(sdnf), " ∧ ".join(sknf), idx_sdnf, idx_sknf

def print_index_form(idx_sdnf, num_rows):
    binary = ['0'] * num_rows
    for i in idx_sdnf:
        binary[i] = '1'
    decimal = 0
    for i in range(num_rows):
        if binary[i] == '1':
            decimal += 2 ** (num_rows - 1 - i) 

    binary_str = ''.join(binary)
    print("Индексная форма:", decimal, "-", binary_str)

