import pytest
import numpy as np
from io import StringIO
from diagonal_adress import DiagonalMatrix, conjunction, sheffer, repeat_first, negate_first

@pytest.fixture
def dm():
    """Фикстура для создания экземпляра DiagonalMatrix с инициализированной матрицей 16x16."""
    dm = DiagonalMatrix()
    grid = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    dm.matrix = np.array(grid, dtype=int)
    return dm

# Тесты для логических функций
def test_conjunction():
    assert conjunction(1, 1) == 1
    assert conjunction(1, 0) == 0
    assert conjunction(0, 1) == 0
    assert conjunction(0, 0) == 0

def test_sheffer():
    assert sheffer(1, 1) == 0
    assert sheffer(1, 0) == 1
    assert sheffer(0, 1) == 1
    assert sheffer(0, 0) == 1

def test_repeat_first():
    assert repeat_first(1, 1) == 1
    assert repeat_first(1, 0) == 1
    assert repeat_first(0, 1) == 0
    assert repeat_first(0, 0) == 0

def test_negate_first():
    assert negate_first(1, 1) == 0
    assert negate_first(1, 0) == 0
    assert negate_first(0, 1) == 1
    assert negate_first(0, 0) == 1

# Тест для метода print_matrix
def test_print_matrix(dm, capsys):
    """Тестирование вывода матрицы."""
    dm.print_matrix()
    captured = capsys.readouterr()
    expected = "\nТекущая матрица:\n" + "\n".join(" ".join(map(str, row)) for row in dm.matrix) + "\n\n"
    assert captured.out == expected

def test_write_word(dm):
    """Тестирование записи слова с учетом диагонального смещения."""
    new_word = [0] * 16
    dm.write_word(0, new_word)
    assert np.array_equal(dm.read_word(0), new_word)
    for i in range(16):
        assert dm.matrix[i, 0] == 0

def test_write_word_invalid_length(dm):
    """Тестирование ошибки при неверной длине слова."""
    with pytest.raises(ValueError, match="Слово должно содержать 16 бит"):
        dm.write_word(0, [0, 1])

def test_write_bit_column(dm):
    """Тестирование записи разрядного столбца."""
    new_col = [1] * 16
    dm.write_bit_column(2, new_col)
    assert np.array_equal(dm.read_bit_column(2), new_col)
    for k in range(16):
        assert dm.matrix[(2 + k) % 16, k] == 1

def test_write_bit_column_invalid_length(dm):
    """Тестирование ошибки при неверной длине столбца."""
    with pytest.raises(ValueError, match="Разрядный столбец должен содержать 16 бит"):
        dm.write_bit_column(0, [0, 1])

def test_logical_operation_columns_conjunction(dm):
    """Тестирование логической операции (конъюнкция) над столбцами."""
    dm.logical_operation_columns(0, 1, 2, conjunction)
    col0 = dm.read_bit_column(0)
    col1 = dm.read_bit_column(1)
    expected = [conjunction(col0[k], col1[k]) for k in range(16)]
    assert np.array_equal(dm.read_bit_column(2), expected)

def test_logical_operation_columns_sheffer(dm):
    """Тестирование логической операции (Шеффер) над столбцами."""
    dm.logical_operation_columns(0, 1, 2, sheffer)
    col0 = dm.read_bit_column(0)
    col1 = dm.read_bit_column(1)
    expected = [sheffer(col0[k], col1[k]) for k in range(16)]
    assert np.array_equal(dm.read_bit_column(2), expected)

def test_logical_operation_columns_repeat_first(dm):
    """Тестирование логической операции (повторение) над столбцами."""
    dm.logical_operation_columns(0, 1, 2, repeat_first)
    expected = dm.read_bit_column(0)
    assert np.array_equal(dm.read_bit_column(2), expected)

def test_logical_operation_columns_negate_first(dm):
    """Тестирование логической операции (отрицание) над столбцами."""
    dm.logical_operation_columns(0, 1, 2, negate_first)
    col0 = dm.read_bit_column(0)
    expected = [negate_first(col0[k], 0) for k in range(16)]
    assert np.array_equal(dm.read_bit_column(2), expected)

def test_logical_operation_words_conjunction(dm):
    """Тестирование логической операции (конъюнкция) над словами."""
    dm.logical_operation_words(2, 3, 15, conjunction)
    word2 = dm.read_word(2)
    word3 = dm.read_word(3)
    expected = [conjunction(word2[i], word3[i]) for i in range(16)]
    assert np.array_equal(dm.read_word(15), expected)

def test_logical_operation_words_sheffer(dm):
    """Тестирование логической операции (Шеффер) над словами."""
    dm.logical_operation_words(2, 3, 15, sheffer)
    word2 = dm.read_word(2)
    word3 = dm.read_word(3)
    expected = [sheffer(word2[i], word3[i]) for i in range(16)]
    assert np.array_equal(dm.read_word(15), expected)

def test_logical_operation_words_repeat_first(dm):
    """Тестирование логической операции (повторение) над словами."""
    dm.logical_operation_words(2, 3, 15, repeat_first)
    expected = dm.read_word(2)
    assert np.array_equal(dm.read_word(15), expected)

def test_logical_operation_words_negate_first(dm):
    """Тестирование логической операции (отрицание) над словами."""
    dm.logical_operation_words(2, 3, 15, negate_first)
    word2 = dm.read_word(2)
    expected = [negate_first(word2[i], 0) for i in range(16)]
    assert np.array_equal(dm.read_word(15), expected)

def test_add_fields(dm):
    """Тестирование сложения полей A и B для слов с заданным V."""
    dm.write_word(0, [1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0])
    dm.add_fields("111")
    word = dm.read_word(0)
    A = int('0011', 2)  # 3
    B = int('0100', 2)  # 4
    S = bin(A + B)[2:].zfill(5)  # 7 = 00111
    expected = [1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1]
    assert np.array_equal(word, expected)

def test_add_fields_invalid_v(dm):
    """Тестирование ошибки при неверной длине V."""
    with pytest.raises(ValueError, match="V должно содержать 3 бита"):
        dm.add_fields("11")

def test_find_nearest_no_candidates(dm):
    """Тестирование поиска при отсутствии подходящих слов."""
    index, word, value = dm.find_nearest("1111111111111111", "above")
    assert index is None
    assert word is None
    assert value == "Нет слов, удовлетворяющих условию"

def test_find_nearest_invalid_a(dm):
    """Тестирование ошибки при неверном формате A."""
    with pytest.raises(ValueError, match="Аргумент A должен быть 16-битным числом"):
        dm.find_nearest("11", "below")