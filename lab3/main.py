from logic_operations import *
from minimization import print_calculation_results
from tabular_computed_minimization import print_tabular_results
from karnaugh_minimization import print_karnaugh_results

def main():
    print("Логический калькулятор (ОПЗ + СДНФ, СКНФ и минимизация)")
    print("Операции: & (и), | (или), ! (не), > (импликация), ~ (эквивалентность)")
    print("Поддерживаемые переменные: до 5 (a, b, c, d, e)")
    print("Пример ввода: (a & b) | (!a > c)")

    while True:
        expression = input("\nВведите логическое выражение (или 'exit' для выхода): ").strip()
        if expression.lower() == 'exit':
            break

        variables, is_valid = function_spellcheck(expression)
        if not is_valid:
            print("Ошибка: Некорректное выражение. Проверьте скобки и допустимые символы.")
            continue
        if not variables:
             print("Ошибка: Выражение не содержит переменных.")
             continue
        if len(variables) > 5:
            print("Ошибка: Поддерживается не более 5 переменных (a, b, c, d, e).")
            continue

        print(f"\n--- Обработка выражения: {expression} ---")
        print(f"Обнаруженные переменные: {', '.join(sorted(variables))}")

        try:
            rpn = shunting_yard(expression)
            print(f"\nОбратная польская запись (ОПЗ): {' '.join(rpn)}")

            table = build_truth_table(expression, variables)
            print(f"\nТаблица истинности ({len(table)-1} строк):")
            print_truth_table(table)

            sdnf, sknf, idx_sdnf, idx_sknf = get_normal_forms(table, variables)
            print("\nСовершенная Дизъюнктивная Нормальная Форма (СДНФ):")
            print(sdnf or "Функция тождественно равна 0")
            print("\nСовершенная Конъюнктивная Нормальная Форма (СКНФ):")
            print(sknf or "Функция тождественно равна 1")

            num_rows = 2**len(variables) 

            if sdnf:
                idx_sdnf_list = idx_sdnf if isinstance(idx_sdnf, list) else [idx_sdnf]
                idx_sdnf_str = f"({', '.join(map(str, idx_sdnf_list))})"
                print("\nЧисловая форма СДНФ (индексы строк со значением 1):", idx_sdnf_str)
                print_index_form(idx_sdnf_list, num_rows) 
            else:
                 print("\nЧисловая форма СДНФ: - (нет строк со значением 1)")
                 print("Индексная форма: 0 - " + '0' * num_rows)


            if sknf:
                idx_sknf_list = idx_sknf if isinstance(idx_sknf, list) else [idx_sknf]
                idx_sknf_str = f"({', '.join(map(str, idx_sknf_list))})"
                print("\nЧисловая форма СКНФ (индексы строк со значением 0):", idx_sknf_str)
            else:
                print("\nЧисловая форма СКНФ: - (нет строк со значением 0)")


            print("\n\n--- Результаты минимизации ---")

            print("\n=== 1. Расчетный метод ===")
            print_calculation_results(expression, variables)

            print("\n=== 2. Расчетно-табличный метод ===")
            print_tabular_results(expression, variables)

            print("\n=== 3. Метод карт Карно ===")
            print_karnaugh_results(expression, variables)

            print("\n--- Обработка завершена ---")

        except Exception as e:
            print(f"\nПроизошла ошибка при обработке выражения: {e}")

if __name__ == "__main__":
    main()