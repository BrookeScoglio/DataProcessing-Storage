class InMemoryDB:
    def __init__(self):
        self.data = {}
        self.transaction_in_progress = False
        self.transaction_data = {}

    def begin_transaction(self):
        if self.transaction_in_progress:
            raise Exception("Transaction already in progress")
        self.transaction_in_progress = True

    def put(self, key, val):
        if not self.transaction_in_progress:
            raise Exception("No transaction in progress")
        self.transaction_data[key] = val

    def get(self, key):
        if key in self.transaction_data:
            return self.transaction_data[key]
        return self.data.get(key)

    def commit(self):
        if not self.transaction_in_progress:
            raise Exception("No transaction in progress")
        self.data.update(self.transaction_data)
        self.transaction_data.clear()
        self.transaction_in_progress = False

    def rollback(self):
        if not self.transaction_in_progress:
            raise Exception("No transaction in progress")
        self.transaction_data.clear()
        self.transaction_in_progress = False


# Example usage
in_memory_db = InMemoryDB()
print(in_memory_db.get("A"))  # Output: None
try:
    in_memory_db.put("A", 5)  # Raises exception
except Exception as e:
    print(e)
in_memory_db.begin_transaction()
in_memory_db.put("A", 5)
print(in_memory_db.get("A"))  # Output: None
in_memory_db.put("A", 6)
in_memory_db.commit()
print(in_memory_db.get("A"))  # Output: 6
try:
    in_memory_db.commit()  # Raises exception
except Exception as e:
    print(e)
try:
    in_memory_db.rollback()  # Raises exception
except Exception as e:
    print(e)
print(in_memory_db.get("B"))  # Output: None
in_memory_db.begin_transaction()
in_memory_db.put("B", 10)
in_memory_db.rollback()
print(in_memory_db.get("B"))  # Output: None
