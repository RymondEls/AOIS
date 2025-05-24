import pytest
from hash_table import HashTable

@pytest.fixture
def hash_table():
    """Create a new HashTable instance for each test."""
    return HashTable(size=10)

@pytest.fixture
def filled_hash_table():
    """Create a HashTable with some initial data."""
    ht = HashTable(size=10)
    terms = [
        ("Квадрат", "Square"),
        ("Круг", "Circle"),
        ("Матрица", "Matrix"),
        ("Интеграл", "Integral")
    ]
    for key, value in terms:
        ht.create(key, value)
    return ht

def test_init(hash_table):
    """Test HashTable initialization."""
    assert hash_table.size == 10
    assert len(hash_table.slots) == 10
    assert len(hash_table.data) == 10
    assert all(slot is None for slot in hash_table.slots)
    assert all(data is None for data in hash_table.data)
    assert len(hash_table.collisions) == 0
    assert len(hash_table.literals) == 33
    assert hash_table.DELETED is not None

def test_v_function_invalid_length(hash_table):
    """Test v_function with keyword length < 2."""
    with pytest.raises(ValueError, match="Неподходящее ключевое значение"):
        hash_table.v_function("К")

def test_v_function_invalid_chars(hash_table):
    """Test v_function with non-Russian characters."""
    with pytest.raises(ValueError, match="Неподходящее ключевое значение"):
        hash_table.v_function("ABC")
    with pytest.raises(ValueError, match="Неподходящее ключевое значение"):
        hash_table.v_function("К1")

def test_hashfunction(hash_table):
    """Test hashfunction."""
    v_value = (12 + 1) * 33 + (2 + 1)  # For "Квадрат"
    assert hash_table.hashfunction(v_value) == v_value % hash_table.size

def test_hash_value_plus_one(hash_table):
    """Test hash_value_plus_one."""
    assert hash_table.hash_value_plus_one(5, 10) == 6
    assert hash_table.hash_value_plus_one(9, 10) == 0

def test_create_new_key(hash_table):
    """Test creating a new key-value pair."""
    hash_table.create("Квадрат", "Square")
    v_value = hash_table.v_function("Квадрат")
    hashvalue = hash_table.hashfunction(v_value)
    assert hash_table.slots[hashvalue] == "Квадрат"
    assert hash_table.data[hashvalue] == "Square"
    assert len(hash_table.collisions) == 0

def test_create_existing_key(hash_table):
    """Test creating with an existing key (updates value)."""
    hash_table.create("Квадрат", "Square")
    hash_table.create("Квадрат", "New Square")
    v_value = hash_table.v_function("Квадрат")
    hashvalue = hash_table.hashfunction(v_value)
    assert hash_table.slots[hashvalue] == "Квадрат"
    assert hash_table.data[hashvalue] == "New Square"
    assert len(hash_table.collisions) == 0


def test_get_existing_key(filled_hash_table):
    """Test getting an existing key."""
    assert filled_hash_table.get("Квадрат") == "Square"
    assert filled_hash_table.get("Интеграл") == "Integral"

def test_get_nonexistent_key(filled_hash_table):
    """Test getting a non-existent key."""
    assert filled_hash_table.get("Несуществующий") is None

def test_update_existing_key(filled_hash_table):
    """Test updating an existing key."""
    assert filled_hash_table.update("Квадрат", "Updated Square") is True
    assert filled_hash_table.get("Квадрат") == "Updated Square"

def test_update_nonexistent_key(hash_table):
    """Test updating a non-existent key."""
    assert hash_table.update("Квадрат", "Square") is False

def test_delete_existing_key(filled_hash_table):
    """Test deleting an existing key."""
    assert filled_hash_table.delete("Квадрат") is True
    assert filled_hash_table.get("Квадрат") is None
    v_value = filled_hash_table.v_function("Квадрат")
    hashvalue = filled_hash_table.hashfunction(v_value)
    assert filled_hash_table.slots[hashvalue] is filled_hash_table.DELETED

def test_delete_nonexistent_key(hash_table):
    """Test deleting a non-existent key."""
    assert hash_table.delete("Квадрат") is False

def test_linear_collision_resolve_put(filled_hash_table):
    """Test linear_collision_resolve_put with collisions."""
    original_collisions = len(filled_hash_table.collisions)
    terms = [("Круг", "New Circle"), ("Косинус", "Cosine")]
    filled_hash_table.linear_collision_resolve_put(terms)
    assert len(filled_hash_table.collisions) == 0
    assert filled_hash_table.get("Круг") == "New Circle"
    assert filled_hash_table.get("Косинус") == "Cosine"

def test_full_table_resize(hash_table):
    """Test resizing when table is full."""
    # Fill table completely
    for i in range(hash_table.size):
        key = f"Ключ{i+1}"  # Ensure valid Russian keys
        if key[0] in hash_table.literals and key[1] in hash_table.literals:
            hash_table.create(key, f"Value{i+1}")
        else:
            hash_table.create(f"Ключ{i+1}А", f"Value{i+1}")
    original_size = hash_table.size
    hash_table.create("Круг", "Circle")
    hash_table.linear_collision_resolve_put([("Круг", "Circle")])
    assert hash_table.size > original_size
    assert hash_table.get("Круг") == "Circle"

def test_operator_overloading(filled_hash_table):
    """Test __getitem__ and __setitem__."""
    filled_hash_table["Квадрат"] = "New Square"
    assert filled_hash_table["Квадрат"] == "New Square"
    assert filled_hash_table["Несуществующий"] is None
