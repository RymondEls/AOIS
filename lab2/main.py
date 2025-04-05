from logic_operations import *

def main():
    print("Логический калькулятор (ОПЗ + СДНФ и СКНФ)")
    print("Операции: & (и), | (или), ! (не), > (импликация), ~ (эквивалентность)")

    while True:
        expression = input("\nВведите логическое выражение (или 'exit'): ").strip()
        if expression.lower() == 'exit':
            break

        variables, is_valid = function_spellcheck(expression)
        if not is_valid:
            print("Ошибка: Некорректное выражение")
            continue
        if len(variables) > 5:
            print("Ошибка: максимум 5 переменных")
            continue

        print(f"Переменные: {', '.join(variables)}")
        rpn = shunting_yard(expression)
        print(f"ОПЗ: {' '.join(rpn)}")

        table = build_truth_table(expression, variables)
        print(f"\nТаблица истинности ({len(table)-1} строк):")
        print_truth_table(table)

        sdnf, sknf, idx_sdnf, idx_sknf = get_normal_forms(table, variables)
        print("\nСДНФ:")
        print(sdnf or "—")
        print("СКНФ:")
        print(sknf or "—")

        print("\nЧисловая форма СДНФ: ", tuple(idx_sdnf))
        print("Числовая форма СКНФ: ", tuple(idx_sknf))

        print_index_form(idx_sdnf, len(table)-1)

if __name__ == "__main__":
    main()