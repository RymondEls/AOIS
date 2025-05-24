from hash_table import HashTable
from prettytable import PrettyTable
import os

def load_terms(file_path):
    """Загрузка биологических терминов из файла."""
    terms = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and ':' in line:
                    key, data = line.split(':', 1)
                    terms.append((key.strip(), data.strip()))
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
    return terms

def print_table(table, title):
    """Print the hash table using PrettyTable."""
    prettytable = PrettyTable()
    prettytable.field_names = ["ID", "Ключ", "Значение"]
    id = 0
    for slot, value in zip(table.slots, table.data):
        if slot is not table.DELETED:
            prettytable.add_row([id, slot, value])
            id+=1
    print(f"\n{title}:")
    print(prettytable)

termins = load_terms('math.txt')

Table = HashTable()
for term in termins:
    Table[term[0]] = term[1]

print_table(Table ,"Исходная хэш-таблица с коллизиями:")

print("Исходная хэш-таблица с коллизиями:")


print("\nКоллизии:")
for collision in Table.collisions:
    print(f"Ключ '{collision[1]}' хочет попасть в ту же ячейку, в которой и ключ '{collision[0]}'")

Table.linear_collision_resolve_put(termins)

print_table(Table, "\nХэш-таблица после разрешения коллизий:")

print("\nОперация Read")
keys_to_read = ["Квадрат", "Интеграл", "Аппроксимация"]
for key in keys_to_read:
    value = Table.get(key)
    print(f"Чтение ключа '{key}': {value}")

print("\nОперация Update")
updates = [
    ("Квадрат", "Четырёхугольник с равными сторонами и углами"),
    ("Интеграл", "Математическая операция для вычисления площадей")
]
for key, value in updates:
    success = Table.update(key, value)
    print(f"Обновление ключа '{key}': {'Успешно' if success else 'Не найдено'}")
print_table(Table, "Хэш-таблица после обновления")

print("\nОперация Delete")
keys_to_delete = ["Координата", "Матрица", "Несуществующий"]
for key in keys_to_delete:
    success = Table.delete(key)
    print(f"Удаление ключа '{key}': {'Успешно' if success else 'Не найдено'}")
print_table(Table, "Хэш-таблица после удаления")