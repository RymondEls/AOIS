from binary_operations import *

def main():
    print("Добро пожаловать в программу для работы с числами!")
    while True:
        print("\nВыберите операцию:")
        print("1. Операции с целыми числами (перевод, сложение, вычитание, умножение, деление)")
        print("2. Сложение чисел с плавающей точкой (IEEE-754)")
        print("3. Выход")
        choice = input("Ваш выбор: ")

        if choice == "1":

            num1 = int(input("Введите первое целое число: "))
            num2 = int(input("Введите второе целое число: "))


            print("\nПеревод в двоичный формат:")
            print(f"Прямой код ({num1}): {decimal_to_signed_magnitude(num1)}")
            print(f"Обратный код ({num1}): {decimal_to_1s_complement(num1)}")
            print(f"Дополнительный код ({num1}): {decimal_to_2s_complement(num1)}")
            print(f"Прямой код ({num2}): {decimal_to_signed_magnitude(num2)}")
            print(f"Обратный код ({num2}): {decimal_to_1s_complement(num2)}")
            print(f"Дополнительный код ({num2}): {decimal_to_2s_complement(num2)}")


            binary_sum, decimal_sum = add_2s_complement(num1, num2)
            print(f"\nСложение ({num1} + {num2}):")
            print(f"Двоичный результат: {binary_sum}")
            print(f"Десятичный результат: {decimal_sum}")

            binary_diff, decimal_diff = subtract_2s_complement(num1, num2)
            print(f"\nВычитание ({num1} - {num2}):")
            print(f"Двоичный результат: {binary_diff}")
            print(f"Десятичный результат: {decimal_diff}")

            binary_mul, decimal_mul = multiply_signed_magnitude(num1, num2)
            print(f"\nУмножение ({num1} * {num2}):")
            print(f"Двоичный результат: {binary_mul}")
            print(f"Десятичный результат: {decimal_mul}")

            if num2 == 0:
                print("\nДеление на ноль невозможно!")
            else:
                binary_div, decimal_div = divide_signed_magnitude(num1, num2)
                print(f"\nДеление ({num1} / {num2}):")
                print(f"Двоичный результат: {binary_div}")
                print(f"Десятичный результат: {decimal_div}")

        elif choice == "2":

            num1 = float(input("Введите первое число с плавающей точкой: "))
            num2 = float(input("Введите второе число с плавающей точкой: "))


            binary_sum = add_ieee754(num1, num2)
            decimal_sum = ieee754_to_decimal(binary_sum)
            print(f"\nСложение IEEE-754 ({num1} + {num2}):")
            print(f"Двоичный результат: {binary_sum}")
            print(f"Десятичный результат: {decimal_sum}")

        elif choice == "3":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")


main()