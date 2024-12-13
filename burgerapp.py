import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from foodsystem import FoodSystem, Order


class BurgerOrderingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Burger Ordering System")
        self.food_system = FoodSystem()
        self.orders = []

        self.create_background()
        self.root.resizable(False, False)
        self.root.geometry("800x500")

        self.create_widgets()

    def create_background(self):
        try:
            self.bg_image = PhotoImage(file="burger.png")
        except Exception as e:
            print(f"Error loading background image: {e}")
            return

        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)

    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=10)

        tk.Label(title_frame, text="BURGER KA", font=("Arial", 18, "bold"), bg="yellow", fg="black").pack(side=tk.LEFT)
        tk.Label(title_frame, text="SAKIN", font=("Arial", 18, "bold"), bg="black", fg="yellow").pack(side=tk.LEFT)

        # Menu Frame
        menu_frame = tk.Frame(self.root, bg="black")
        menu_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(menu_frame, text="Menu", font=("Arial", 14, "bold"), bg="yellow").pack()
        self.menu_listbox = tk.Listbox(menu_frame, width=40, height=15)
        self.menu_listbox.pack()

        # Populate Menu
        for item in self.food_system.food_items:
            self.menu_listbox.insert(tk.END, f"{item.food_id} - {item.name} (Php{item.price:.2f})")

        # Add to Order
        tk.Label(menu_frame, text="Quantity:", bg="yellow").pack(pady=5)
        self.quantity_var = tk.IntVar(value=1)
        tk.Entry(menu_frame, textvariable=self.quantity_var, width=5).pack()

        tk.Button(menu_frame, text="Add to Order", command=self.add_to_order, bg="yellow").pack(pady=10)

        # Order Frame
        order_frame = tk.Frame(self.root, bg="black")
        order_frame.pack(side=tk.RIGHT, padx=50)

        tk.Label(order_frame, text="Your Order", font=("Arial", 14, "bold"), bg="yellow").pack()
        self.order_tree = ttk.Treeview(order_frame, columns=("Item", "Qty", "Price"), show="headings")
        self.order_tree.heading("Item", text="Item")
        self.order_tree.heading("Qty", text="Qty")
        self.order_tree.heading("Price", text="Price")

        self.order_tree.column("Item", width=200, anchor="w")
        self.order_tree.column("Qty", width=50, anchor="center")
        self.order_tree.column("Price", width=100, anchor="center")

        self.order_tree.pack()

        # Receipt and Controls
        tk.Button(order_frame, text="Generate Receipt", command=self.generate_receipt, bg="yellow").pack(pady=5)
        tk.Button(order_frame, text="Clear Orders", command=self.clear_orders, bg="yellow").pack(pady=5)

    def add_to_order(self):
        selected = self.menu_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item from the menu.")
            return

        item_text = self.menu_listbox.get(selected[0])
        food_id = item_text.split(" - ")[0]
        food_item = self.food_system.get_food_by_id(food_id)
        if not food_item:
            messagebox.showerror("Error", "Invalid Food ID.")
            return

        quantity = self.quantity_var.get()
        if quantity <= 0:
            messagebox.showwarning("Invalid Quantity", "Quantity must be greater than zero.")
            return

        order = Order(food_item, quantity)
        self.orders.append(order)
        self.update_order_list()

    def update_order_list(self):
        for row in self.order_tree.get_children():
            self.order_tree.delete(row)

        total_cost = 0
        for order in self.orders:
            cost = order.food_item.price * order.quantity
            total_cost += cost
            self.order_tree.insert("", tk.END, values=(order.food_item.name, order.quantity, f"Php{cost:.2f}"))

    def generate_receipt(self):
        if not self.orders:
            messagebox.showwarning("No Orders", "Your order list is empty.")
            return

        receipt = "*****************************\n"
        receipt += "        BURGER KA SAKIN\n"
        receipt += "     Thank you for ordering! \n"
        receipt += "*****************************\n\n"

        total_cost = 0
        for order in self.orders:
            item_cost = order.food_item.price * order.quantity
            receipt += f"{order.food_item.name} (x{order.quantity}) - Php{item_cost:.2f}\n"
            total_cost += item_cost

        receipt += "\n----------------------------------\n"
        discount = 0
        if messagebox.askyesno("Discount", "Apply a 10% discount?"):
            discount = total_cost * 0.10
            total_cost -= discount
            receipt += f"Discount: - Php{discount:.2f}\n"

        receipt += f"\nTotal Cost: Php{total_cost:.2f}\n"
        receipt += "*****************************\n"
        receipt += "  Payment Method: Cash/Card\n"
        receipt += "*****************************\n"
        receipt += "   Thank you for your order!\n"
        receipt += "*****************************\n"

        messagebox.showinfo("Receipt", receipt)
        self.clear_orders()

    def clear_orders(self):
        self.orders.clear()
        self.update_order_list()
