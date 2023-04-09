import uuid
class Product():
    def __init__(self, name, expiry, category):
        self.name = name
        self.expiry = expiry
        self.category = category
        self.product_id = str(uuid.uuid4())
        self.serialNumber = str(uuid.uuid4())
        self.quantity = 12
        self.inventoryLog = []
        self.price = 100