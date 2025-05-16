import sys, os
sys.path.append(os.getcwd())
from lab3.src.logic_operations import *
from lab3.src.minimization import *

truth_table_data = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1]
]


def print_truth_table():
    """Выводит таблицу истинности для ОДС-3."""
    print("\nТаблица истинности для ОДС-3:")
    header = "A | B | Cin | S | Cout"
    print(header)
    print("-" * len(header))
    for row in truth_table_data:
        print(f"{row[0]} | {row[1]} |  {row[2]}  | {row[3]} |  {row[4]}")

def main():
    print_truth_table()

    variables = ['a', 'b', 'c'] 

    s_output_table = [row[:-1] for row in truth_table_data] 
    result_output_table = [[row[0]] + [row[1]] + [row[2]] + [row[-1]] for row in truth_table_data]

    s_sdnf, s_sknf, idx_sdnf, idx_sknf = get_normal_forms(s_output_table, variables)
    print("\nСДНФ для S:")
    print(s_sdnf)

    s_sdnf = s_sdnf.replace("∨", "|").replace("∧", "&").replace("¬", "!")
    _, s_minimized = minimize_calculation(s_sdnf, variables, "SDNF")
    print("\nМинимизированная ДНФ для S:")
    dnf_to_print = "("
    for char in s_minimized:
        if char == "∨":
            dnf_to_print = ''.join([dnf_to_print, ')', '∨', '('])
        else:
            dnf_to_print = ''.join([dnf_to_print, char])
    dnf_to_print = dnf_to_print + ")"
    print(dnf_to_print)

    result_sdnf, result_sknf, idx_sdnf, idx_sknf = get_normal_forms(result_output_table, variables)
    print("\nСДНФ для Cout:")
    print(result_sdnf)

    result_sdnf = result_sdnf.replace("∨", "|").replace("∧", "&").replace("¬", "!")
    _, result_minimized = minimize_calculation(result_sdnf, variables, "SDNF")
    print("\nМинимизированная ДНФ для Cout:")
    dnf_to_print = "("
    for char in result_minimized:
        if char == "∨":
            dnf_to_print = ''.join([dnf_to_print, ')', ' ∨ ', '('])
        else:
            dnf_to_print = ''.join([dnf_to_print, char])
    dnf_to_print = dnf_to_print + ")"
    print(dnf_to_print)



if __name__ == "__main__":
    main()