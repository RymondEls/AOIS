import numpy as np

def conjunction(x, y):
    return x and y

def sheffer(x, y):
    return not (x and y)

def repeat_first(x, y):
    return x

def negate_first(x, y):
    return not x

class DiagonalMatrix:
    def __init__(self):
        self.size = 16
        self.matrix = np.zeros((self.size, self.size), dtype=int)

    def read_word(self, k):
        if not 0 <= k < self.size:
            raise ValueError("Индекс слова должен быть от 0 до 15")
        return [self.matrix[(i + k) % self.size, k] for i in range(self.size)]

    def write_word(self, k, word):
        if not 0 <= k < self.size:
            raise ValueError("Индекс слова должен быть от 0 до 15")
        if len(word) != self.size:
            raise ValueError("Слово должно содержать 16 бит")
        if not all(bit in (0, 1) for bit in word):
            raise ValueError("Слово должно состоять только из 0 и 1")
        for i in range(self.size):
            self.matrix[(i + k) % self.size, k] = word[i]

    def read_bit_column(self, i):
        if not 0 <= i < self.size:
            raise ValueError("Индекс разряда должен быть от 0 до 15")
        return [self.matrix[(i + k) % self.size, k] for k in range(self.size)]

    def write_bit_column(self, i, column):
        if not 0 <= i < self.size:
            raise ValueError("Индекс разряда должен быть от 0 до 15")
        if len(column) != self.size:
            raise ValueError("Разрядный столбец должен содержать 16 бит")
        if not all(bit in (0, 1) for bit in column):
            raise ValueError("Столбец должен состоять только из 0 и 1")
        for k in range(self.size):
            self.matrix[(i + k) % self.size, k] = column[k]

    def logical_operation_columns(self, a, b, c, operation):
        if not all(0 <= x < self.size for x in (a, b, c)):
            raise ValueError("Индексы разрядов должны быть от 0 до 15")
        col_a = self.read_bit_column(a)
        col_b = self.read_bit_column(b)
        result = [operation(col_a[k], col_b[k]) for k in range(self.size)]
        self.write_bit_column(c, result)

    def logical_operation_words(self, w1, w2, target, operation):
        if not all(0 <= x < self.size for x in (w1, w2, target)):
            raise ValueError("Индексы слов должны быть от 0 до 15")
        word1 = self.read_word(w1)
        word2 = self.read_word(w2)
        result = [operation(word1[i], word2[i]) for i in range(self.size)]
        self.write_word(target, result)
        return result

    def add_fields(self, v):
        if len(v) != 3 or not all(c in '01' for c in v):
            raise ValueError("V должно содержать 3 бита")
        v_bits = [int(c) for c in v]
        updated = []
        for k in range(self.size):
            word = self.read_word(k)
            if word[:3] == v_bits:
                A = int(''.join(map(str, word[3:7])), 2)
                B = int(''.join(map(str, word[7:11])), 2)
                S = A + B
                S_bits = [int(b) for b in bin(S)[2:].zfill(5)]
                new_word = word[:11] + S_bits
                self.write_word(k, new_word)
                updated.append(k)
        return updated

    def find_nearest(self, a, direction):
        if len(a) != self.size or not all(c in '01' for c in a):
            raise ValueError("Аргумент A должен быть 16-битным числом")
        a_bits = [int(c) for c in a]
        g = [0] * self.size
        l = [0] * self.size
        for i in range(self.size - 1, -1, -1):
            new_g = [0] * self.size
            new_l = [0] * self.size
            for j in range(self.size):
                S_j_i = self.matrix[(i + j) % self.size, j]
                if i == self.size - 1:
                    new_g[j] = (not a_bits[i]) and S_j_i
                    new_l[j] = a_bits[i] and (not S_j_i)
                else:
                    new_g[j] = g[j] or ((not a_bits[i]) and S_j_i and (not g[j]))
                    new_l[j] = l[j] or (a_bits[i] and (not S_j_i) and (not g[j]))
            g, new_g = new_g, g
            l, new_l = new_l, l
        candidates = []
        for j in range(self.size):
            word = self.read_word(j)
            value = int(''.join(map(str, word)), 2)
            if direction == "below" and l[j]:
                candidates.append((value, j, word))
            elif direction == "above" and g[j]:
                candidates.append((value, j, word))
        if not candidates:
            return None, None, "Нет слов, удовлетворяющих условию"
        if direction == "below":
            value, index, word = max(candidates)
        else:
            value, index, word = min(candidates)
        return index, word, value

    def print_matrix(self):
        print("\nТекущая матрица:")
        for row in self.matrix:
            print(" ".join(map(str, row)))
        print()
