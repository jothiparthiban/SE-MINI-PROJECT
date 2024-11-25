import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

# Database initialization function
def init_db():
    conn = sqlite3.connect('courier_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        phone TEXT NOT NULL
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS couriers (
        courier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        pickup_location TEXT NOT NULL,
        delivery_location TEXT NOT NULL,
        weight REAL NOT NULL,
        price REAL NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )''')
    conn.commit()
    conn.close()

# Function to add a customer
def add_customer(name, address, phone):
    conn = sqlite3.connect('courier_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO customers (name, address, phone) VALUES (?, ?, ?)', (name, address, phone))
    customer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return customer_id

# Function to calculate price based on weight
def calculate_price(weight):
    return weight * 10  # Example pricing calculation

# Function to add a courier
def add_courier(customer_id, pickup_location, delivery_location, weight, status):
    price = calculate_price(weight)
    conn = sqlite3.connect('courier_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO couriers (customer_id, pickup_location, delivery_location, weight, price, status) VALUES (?, ?, ?, ?, ?, ?)', 
                   (customer_id, pickup_location, delivery_location, weight, price, status))
    courier_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return courier_id, customer_id, pickup_location, delivery_location, weight, price, status

# Function to refresh the courier table
def refresh_courier_table():
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect('courier_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM couriers')
    couriers = cursor.fetchall()
    for courier in couriers:
        tree.insert("", "end", values=courier)
    conn.close()

# GUI function to add a customer
def add_customer_gui():
    name = entry_name.get()
    address = entry_address.get()
    phone = entry_phone.get()
    if name and address and phone:
        customer_id = add_customer(name, address, phone)
        messagebox.showinfo("Success", f"Customer added successfully. Customer ID: {customer_id}")
    else:
        messagebox.showwarning("Input Error", "All fields are required")

# GUI function to add a courier
def add_courier_gui():
    customer_id = entry_customer_id.get()
    pickup_location = entry_pickup_location.get()
    delivery_location = entry_delivery_location.get()
    weight = entry_weight.get()
    status = entry_status.get()
    if customer_id and pickup_location and delivery_location and weight and status:
        try:
            weight = float(weight)
            courier_details = add_courier(customer_id, pickup_location, delivery_location, weight, status)
            messagebox.showinfo("Success", f"Courier added successfully. Courier Details: {courier_details}")
            refresh_courier_table()
        except ValueError:
            messagebox.showwarning("Input Error", "Weight must be a number")
    else:
        messagebox.showwarning("Input Error", "All fields are required")

# Initialize the main window
root = Tk()
root.title("Courier Management System")
root.geometry("800x600")  # Make the GUI bigger

# Customer Form
frame_customer = Frame(root)
frame_customer.pack(pady=10)

label_name = Label(frame_customer, text="Customer Name")
label_name.grid(row=0, column=0, padx=5, pady=5)
entry_name = Entry(frame_customer)
entry_name.grid(row=0, column=1, padx=5, pady=5)

label_address = Label(frame_customer, text="Customer Address")
label_address.grid(row=1, column=0, padx=5, pady=5)
entry_address = Entry(frame_customer)
entry_address.grid(row=1, column=1, padx=5, pady=5)

label_phone = Label(frame_customer, text="Customer Phone")
label_phone.grid(row=2, column=0, padx=5, pady=5)
entry_phone = Entry(frame_customer)
entry_phone.grid(row=2, column=1, padx=5, pady=5)

button_add_customer = Button(frame_customer, text="Add Customer", command=add_customer_gui)
button_add_customer.grid(row=3, columnspan=2, pady=10)

# Courier Form
frame_courier = Frame(root)
frame_courier.pack(pady=10)

label_customer_id = Label(frame_courier, text="Customer ID")
label_customer_id.grid(row=0, column=0, padx=5, pady=5)
entry_customer_id = Entry(frame_courier)
entry_customer_id.grid(row=0, column=1, padx=5, pady=5)

label_pickup_location = Label(frame_courier, text="Pickup Location")
label_pickup_location.grid(row=1, column=0, padx=5, pady=5)
entry_pickup_location = Entry(frame_courier)
entry_pickup_location.grid(row=1, column=1, padx=5, pady=5)

label_delivery_location = Label(frame_courier, text="Delivery Location")
label_delivery_location.grid(row=2, column=0, padx=5, pady=5)
entry_delivery_location = Entry(frame_courier)
entry_delivery_location.grid(row=2, column=1, padx=5, pady=5)

label_weight = Label(frame_courier, text="Weight (kg)")
label_weight.grid(row=3, column=0, padx=5, pady=5)
entry_weight = Entry(frame_courier)
entry_weight.grid(row=3, column=1, padx=5, pady=5)

label_status = Label(frame_courier, text="Status")
label_status.grid(row=4, column=0, padx=5, pady=5)
entry_status = Entry(frame_courier)
entry_status.grid(row=4, column=1, padx=5, pady=5)

button_add_courier = Button(frame_courier, text="Add Courier", command=add_courier_gui)
button_add_courier.grid(row=5, columnspan=2, pady=10)

# Courier Table
frame_table = Frame(root)
frame_table.pack(pady=20)

tree = ttk.Treeview(frame_table, columns=("courier_id", "customer_id", "pickup_location", "delivery_location", "weight", "price", "status"), show='headings')
tree.heading("courier_id", text="Courier ID")
tree.heading("customer_id", text="Customer ID")
tree.heading("pickup_location", text="Pickup Location")
tree.heading("delivery_location", text="Delivery Location")
tree.heading("weight", text="Weight (kg)")
tree.heading("price", text="Price")
tree.heading("status", text="Status")
tree.pack()

# Initialize the database
init_db()

# Load existing couriers into the table
refresh_courier_table()

# Run the main loop
root.mainloop()
