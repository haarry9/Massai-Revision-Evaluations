
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} - Price: {self.price}, Quantiy: {self.quantity}"

    def __add__(self, other):
        # check if the names are the same
        if self.name.lower() == other.name.lower():
            total_qty = self.quantity + other.quantity
            avg_price = (self.price + other.price)/2
            return Product(self.name, avg_price, total_qty)
        else:
            print("Products with same name does not exist!")

    def __lt__(self,other):
        # compare based on the price
        return self.price < other.price
    
class Inventory:
    # list of products
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)
    
    def __len__(self):
        return len(self.products)

    def __getitem__(self, index):
        return self.products[index]
    
    def search_by_name(self, name):
        result = []
        for p in self.products:
            if name.lower() in p.name.lower():
                result.append(p)
        return result
    

inv_obj = Inventory()

inv_obj.add_product(Product("Smart Phone", 45000, 6))
inv_obj.add_product(Product("Laptop", 80000, 6))
inv_obj.add_product(Product("Headphone", 15000, 8))
inv_obj.add_product(Product("Keyboard", 5000, 10))

print("All products sorted by price")
for p in inv_obj.products:
    print(p)

    