class HashTable:
    def __init__(self, initial_size=10, max_bucket_size=5):
        self.size = initial_size
        self.max_bucket_size = max_bucket_size
        self.table = [[] for _ in range(initial_size)]

    # Function that returns the index of the bucket based on the key
    def _hash(self, key):
        return hash(key) % self.size

    # Function to resize the table
    def _resize(self, new_size):
        temp_table = self.table
        self.size = new_size
        self.table = [[] for _ in range(new_size)]
        for b in temp_table:
            if b is not None:
                for key, value in b:
                    self.insert(key, value, True)

    # Function to insert a key-value pair or update the value if the key already exists
    def insert(self, key, value, resize=False):
        index = self._hash(key)
        b = self.table[index]

        for i, (k, _) in enumerate(b):
            # If key already exists, update the value
            if k == key:
                b[i] = (key, value)
                return

        b.append((key, value))

        if not resize and len(b) > self.max_bucket_size:
            self._resize(self.size * 2)

    # Function to lookup a value based on a key
    def lookup(self, key):
        index = self._hash(key)
        b = self.table[index]
        for k, v in b:
            if k == key:
                return v
        return None

    def print_all_values(self):
        for bucket in self.table:
            for item in bucket:
                _, value = item
                print(value)
