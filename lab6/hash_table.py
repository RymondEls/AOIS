class HashTable:
    def __init__(self, size=30):
        self.size = size
        self.slots = [None] * self.size
        self.data = [None] * self.size
        self.literals = [
            'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й',
            'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
            'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я'
        ]
        self.collisions = []
        self.DELETED = object()

    def create(self, key, data):
        """Create a new key-value pair in the hash table."""
        v_value = self.v_function(key)
        hashvalue = self.hashfunction(v_value)

        if self.slots[hashvalue] is None or self.slots[hashvalue] is self.DELETED:
            self.slots[hashvalue] = key
            self.data[hashvalue] = data
        else:
            if self.slots[hashvalue] == key:
                self.data[hashvalue] = data
            else:
                first_collision_item = self.slots[hashvalue]
                self.collisions.append((first_collision_item, key, data))

    def update(self, key, data):
        """Update the value associated with a key."""
        v_value = self.v_function(key)
        hashvalue = self.hashfunction(v_value)
        start_index = hashvalue
        position = hashvalue

        while self.slots[position] is not None:
            if self.slots[position] == key:
                self.data[position] = data
                return True
            position = self.hash_value_plus_one(position, self.size)
            if position == start_index:
                break
        return False

    def delete(self, key):
        """Delete a key-value pair from the hash table."""
        v_value = self.v_function(key)
        hashvalue = self.hashfunction(v_value)
        start_index = hashvalue
        position = hashvalue

        while self.slots[position] is not None:
            if self.slots[position] == key:
                self.slots[position] = self.DELETED
                self.data[position] = None
                return True
            position = self.hash_value_plus_one(position, self.size)
            if position == start_index:
                break
        return False

    def v_function(self, keyword: str):
        if len(keyword) < 2:
            raise ValueError("Неподходящее ключевое значение (длина должна быть не меньше 2 символов)")
        char_one, char_two = keyword[0].upper(), keyword[1].upper()
        if char_one not in self.literals or char_two not in self.literals:
            raise ValueError("Неподходящее ключевое значение (должно быть слово русского языка)")
        v_value = (self.literals.index(char_one) + 1) * 33 + (self.literals.index(char_two) + 1)
        return v_value

    def hashfunction(self, v_value):
        return v_value % self.size

    def hash_value_plus_one(self, oldhash, size):
        return (oldhash + 1) % size

    def rehash_table(self):
        """Double the table size and rehash all existing items."""
        old_items = [(key, value) for key, value in zip(self.slots, self.data) 
                     if key is not None and key is not self.DELETED]
        self.size = self.size * 2
        self.slots = [None] * self.size
        self.data = [None] * self.size
        self.collisions = []
        for key, value in old_items:
            self.create(key, value)

    def linear_consistent_collision(self, key, data):
        """Resolve a collision using linear probing."""
        v_value = self.v_function(key)
        hashvalue = self.hashfunction(v_value)
        start_index = hashvalue
        nextslot = hashvalue

        while True:
            if self.slots[nextslot] is None or self.slots[nextslot] is self.DELETED:
                self.slots[nextslot] = key
                self.data[nextslot] = data
                return
            elif self.slots[nextslot] == key:
                self.data[nextslot] = data
                return
            nextslot = self.hash_value_plus_one(nextslot, self.size)
            if nextslot == start_index:
                self.rehash_table()
                self.linear_consistent_collision(key, data)
                return

    def linear_collision_resolve_put(self, terms):
        """Insert all terms and resolve collisions."""
        for term in terms:
            self.create(term[0], term[1])
        
        while self.collisions:
            collision = self.collisions.pop(0)
            key, data = collision[1], collision[2]
            self.linear_consistent_collision(key, data)

    def get(self, key):
        """Read the value associated with a key."""
        v_value = self.v_function(key)
        startslot = self.hashfunction(v_value)
        position = startslot

        while self.slots[position] is not None:
            if self.slots[position] == key:
                return self.data[position]
            position = self.hash_value_plus_one(position, self.size)
            if position == startslot:
                break
        return None

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, data):
        self.create(key, data)