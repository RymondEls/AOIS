from diagonal_adress import *

def main():
    dm = DiagonalMatrix()
    dm.matrix = np.random.randint(0, 2, size=(16, 16))
    print("Сгенерирована случайная матрица 16x16:")
    dm.print_matrix()

    operations = {
        1: lambda: read_word_operation(dm),
        2: lambda: write_word_operation(dm),
        3: lambda: read_bit_column_operation(dm),
        4: lambda: write_bit_column_operation(dm),
        5: lambda: logical_operation_columns(dm),
        6: lambda: logical_operation_words(dm),
        7: lambda: add_fields_operation(dm),
        8: lambda: find_nearest_operation(dm),
        9: lambda: None
    }

    while True:
        print("\nМеню:")
        print("1. Чтение слова по индексу")
        print("2. Запись слова по индексу")
        print("3. Чтение разрядного столбца по индексу")
        print("4. Запись разрядного столбца по индексу")
        print("5. Логическая операция над разрядными столбцами")
        print("6. Логическая операция над словами")
        print("7. Сложение полей A и B для слов с заданным V")
        print("8. Поиск ближайшего значения сверху или снизу")
        print("9. Выход")
        
        try:
            choice = int(input("Выберите операцию (1-9): "))
            if choice not in operations:
                print("Неверный выбор. Введите число от 1 до 9.")
                continue
            if choice == 9:
                print("Программа завершена.")
                break
            operations[choice]()
            if choice != 9:
                dm.print_matrix()
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

def read_word_operation(dm):
    k = int(input("Введите индекс слова (0-15): "))
    word = dm.read_word(k)
    print(f"Слово {k}: {''.join(map(str, word))}")

def write_word_operation(dm):
    k = int(input("Введите индекс слова (0-15): "))
    word = input("Введите 16-битное слово (например, 0010000000010000): ")
    word_bits = [int(c) for c in word]
    dm.write_word(k, word_bits)
    print(f"Слово {k} успешно записано.")

def read_bit_column_operation(dm):
    i = int(input("Введите индекс разряда (0-15): "))
    col = dm.read_bit_column(i)
    print(f"Разрядный столбец {i}: {''.join(map(str, col))}")

def write_bit_column_operation(dm):
    i = int(input("Введите индекс разряда (0-15): "))
    col = input("Введите 16-битный разрядный столбец (например, 1111111111111111): ")
    col_bits = [int(c) for c in col]
    dm.write_bit_column(i, col_bits)
    print(f"Разрядный столбец {i} успешно записан.")

def logical_operation_columns(dm):
    a = int(input("Введите индекс первого разрядного столбца (0-15): "))
    b = int(input("Введите индекс второго разрядного столбца (0-15): "))
    c = int(input("Введите индекс целевого разрядного столбца (0-15): "))
    print("Выберите операцию:")
    print("1. Конъюнкция")
    print("2. Операция Шеффера")
    print("3. Повторение первого аргумента")
    print("4. Отрицание первого аргумента")
    op_choice = int(input("Введите номер операции (1-4): "))
    operations = {1: conjunction, 2: sheffer, 3: repeat_first, 4: negate_first}
    if op_choice not in operations:
        raise ValueError("Неверный выбор операции")
    dm.logical_operation_columns(a, b, c, operations[op_choice])
    print(f"Логическая операция выполнена, результат записан в столбец {c}.")

def logical_operation_words(dm):
    w1 = int(input("Введите индекс первого слова (0-15): "))
    w2 = int(input("Введите индекс второго слова (0-15): "))
    target = int(input("Введите индекс целевого слова (0-15): "))
    print("Выберите операцию:")
    print("1. Конъюнкция")
    print("2. Операция Шеффера")
    print("3. Повторение первого аргумента")
    print("4. Отрицание первого аргумента")
    op_choice = int(input("Введите номер операции (1-4): "))
    operations = {1: conjunction, 2: sheffer, 3: repeat_first, 4: negate_first}
    if op_choice not in operations:
        raise ValueError("Неверный выбор операции")
    result = dm.logical_operation_words(w1, w2, target, operations[op_choice])
    if result is not None:
        print(f"Результат операции: {''.join(map(str, result))}")
    else:
        raise ValueError("Ошибка выполнения логической операции над словами")

def add_fields_operation(dm):
    v = input("Введите 3-битное значение V (например, 111): ")
    updated = dm.add_fields(v)
    if updated:
        print(f"Обновлены слова с индексами: {', '.join(map(str, updated))}")
    else:
        print("Нет слов с заданным V.")

def find_nearest_operation(dm):
    a = input("Введите 16-битное значение A (например, 0010000000010000): ")
    direction = input("Введите направление поиска (1 - снизу, 2 - сверху): ")
    direction_map = {"1": "below", "2": "above"}
    if direction not in direction_map:
        raise ValueError("Направление должно быть 1 или 2")
    index, word, value = dm.find_nearest(a, direction_map[direction])
    if index is not None:
        print(f"Найдено ближайшее значение: слово {index} = {''.join(map(str, word))} (десятичное: {value})")
    else:
        print(value)

main()