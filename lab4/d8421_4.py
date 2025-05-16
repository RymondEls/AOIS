import sys, os
sys.path.append(os.getcwd())
from lab3.src.logic_operations import *
from lab3.src.minimization import *

# Таблица истинности для преобразователя Д8421 → Д8421+5
# A, B, C, D — входы
# W, X, Y, Z — выходы
truth_table_data = [
    [0, 0, 0, 0, 0, 1, 0, 0],  # 0 → 4
    [0, 0, 0, 1, 0, 1, 0, 1],  # 1 → 5
    [0, 0, 1, 0, 0, 1, 1, 0],  # 2 → 6
    [0, 0, 1, 1, 0, 1, 1, 1],  # 3 → 7
    [0, 1, 0, 0, 1, 0, 0, 0],  # 4 → 8
    [0, 1, 0, 1, 1, 0, 0, 1],  # 5 → 9
    [0, 1, 1, 0, 0, 0, 0, 0],  # 6 → 0
    [0, 1, 1, 1, 0, 0, 0, 1],  # 7 → 1
    [1, 0, 0, 0, 0, 0, 1, 0],  # 8 → 2
    [1, 0, 0, 1, 0, 0, 1, 1],  # 9 → 3
    [1, 0, 1, 0, None, None, None, None],
    [1, 0, 1, 1, None, None, None, None],
    [1, 1, 0, 0, None, None, None, None],
    [1, 1, 0, 1, None, None, None, None],
    [1, 1, 1, 0, None, None, None, None],
    [1, 1, 1, 1, None, None, None, None]
]

def print_truth_table():
    print("\nТаблица истинности для преобразователя Д8421 → Д8421+4:")
    header = "A | B | C | D | W | X | Y | Z"
    print(header)
    print("-" * len(header))
    for row in truth_table_data:
        w = 'X' if row[4] is None else row[4]
        x = 'X' if row[5] is None else row[5]
        y = 'X' if row[6] is None else row[6]
        z = 'X' if row[7] is None else row[7]
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {w} | {x} | {y} | {z}")

def main():
    tables = []
    tables.append([[row[0]] + [row[1]] + [row[2]] + [row[3]] + [row[4]] for row in truth_table_data])
    tables.append([[row[0]] + [row[1]] + [row[2]] + [row[3]] + [row[5]] for row in truth_table_data])
    tables.append([[row[0]] + [row[1]] + [row[2]] + [row[3]] + [row[6]] for row in truth_table_data])
    tables.append([[row[0]] + [row[1]] + [row[2]] + [row[3]] + [row[7]] for row in truth_table_data])
    print_truth_table()
    variables = ['a', 'b', 'c', 'd']
    outputs = ["W", "X", "Y", "Z"]
    index = 0
  
    for table in tables:
        char = outputs[index]
        s_sdnf, s_sknf, idx_sdnf, idx_sknf = get_normal_forms(table, variables)
        print(f"\nСДНФ для {char}:")
        print(s_sdnf)

        s_sdnf = s_sdnf.replace("∨", "|").replace("∧", "&").replace("¬", "!")
        _, s_minimized = minimize_calculation(s_sdnf, variables, "SDNF")
        print(f"\nМинимизированная ДНФ для {char}:")
        dnf_to_print = "("
        for char in s_minimized:
            if char == "∨":
                dnf_to_print = ''.join([dnf_to_print, ')', '∨', '('])
            else:
                dnf_to_print = ''.join([dnf_to_print, char])
        dnf_to_print = dnf_to_print + ")"
        print(dnf_to_print)
        index += 1


if __name__ == "__main__":
    main()