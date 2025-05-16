import sys, os
sys.path.append(os.getcwd())
from lab3.src.minimization import *


def print_truth_table(variables, table, output_name):
    print(f"\nТаблица истинности для {output_name}:")
    header = ' | '.join(variables) + f' | {output_name}'
    print(header)
    print('-' * len(header))
    for values in table:
        row = ' | '.join(map(str, values[:-1])) + f' | {values[-1]}'
        print(row)

def get_normal_forms(table, variables):
    sdnf = []
    sknf = []
    idx_sdnf = []
    idx_sknf = []

    for i, row in enumerate(table[0:]):
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
                terms.append(f"{'¬' + var if val else var}")
            sknf.append("(" + "∨".join(terms) + ")")

    idx_sdnf_result = idx_sdnf[0] if len(idx_sdnf) == 1 else idx_sdnf
    idx_sknf_result = idx_sknf[0] if len(idx_sknf) == 1 else idx_sknf

    return " ∨ ".join(sdnf), " ∧ ".join(sknf), idx_sdnf_result, idx_sknf_result


variables = ['a', 'b', 'c', 'd'] 

truth_tables = [
    [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 1, 1, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 0, 1, 0],
        [1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0]
    ],
    [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 1, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 1, 1, 0],
        [1, 1, 0, 0, 1],
        [1, 1, 0, 1, 0],
        [1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0]
    ],
    [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 1],
        [0, 0, 1, 1, 0],
        [0, 1, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 0, 1],
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 1, 0],
        [1, 1, 0, 0, 1],
        [1, 1, 0, 1, 0],
        [1, 1, 1, 0, 1],
        [1, 1, 1, 1, 0]
    ],
    [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 1, 0, 1],
        [0, 0, 1, 1, 1],
        [0, 1, 0, 0, 1],
        [0, 1, 0, 1, 1],
        [0, 1, 1, 0, 1],
        [0, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1],
        [1, 1, 0, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1]
    ]
]

outputs = ['T3', 'T2', 'T1', 'T0']
index = 0
results = {}
for truth_table in truth_tables:
    output = outputs[index]
    print_truth_table(variables, truth_table, output)
    s_sdnf, s_sknf, idx_sdnf, idx_sknf = get_normal_forms(truth_table, variables)
    print(f"\nСДНФ для {output}:")
    print(s_sdnf)

    s_sdnf = s_sdnf.replace("∨", "|").replace("∧", "&").replace("¬", "!")
    _, s_minimized = minimize_calculation(s_sdnf, variables, "SDNF")
    print(f"\nМинимизированная ДНФ для {output}:")
    dnf_to_print = "("
    for char in s_minimized:
        if char == "∨":
            dnf_to_print = ''.join([dnf_to_print, ')', '∨', '('])
        else:
            dnf_to_print = ''.join([dnf_to_print, char])
    dnf_to_print = dnf_to_print + ")"
    print(dnf_to_print)
    index += 1