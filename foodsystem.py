class FoodItem:
    def __init__(self, food_id, name, price):
        self.food_id = food_id
        self.name = name
        self.price = price
        
class Order:
    def __init__(self, food_item, quantity):
        self.food_item = food_item
        self.quantity = quantity
        
class FoodSystem:
    def __init__(self):
        self.food_items = [
            FoodItem("B1", "Classic Burger", 25.00),
            FoodItem("B2", "Classic CheeseBurger", 30.00),
            FoodItem("B3", "Grilled Cheese Burger", 45.00),
            FoodItem("B4", "Juicy Whopper", 55.00),
            FoodItem("B5", "Aloha Burger", 90.00),
            FoodItem("B6", "Bacon and Cheese Sandwich", 85.00),
            FoodItem("S1", "Fries", 60.00),
            FoodItem("S2", "Onion Rings", 50.00),
            FoodItem("D1", "Coke", 30.00),
            FoodItem("D2", "Sparkling Water", 30.00),
            FoodItem("D3", "Nestea", 30.00),
        ]

    def get_food_by_id(self, food_id):
        for item in self.food_items:
            if item.food_id == food_id:
                return item
        return None
   