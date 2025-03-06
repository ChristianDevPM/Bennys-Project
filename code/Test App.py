import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class PoolHallApp:
    def __init__(self, root):
        print("Initializing the application...")  # Debugging initialization
        self.root = root
        self.root.title("Benny's Billiards Table Rental System")
        self.root.geometry("600x600")  # Make window bigger for all buttons
        self.pricing = {'basic': 20, 'league': 30}
        self.rentals = {}
        self.selected_table = None  # Track the currently selected table
        self.create_widgets()

    def create_widgets(self):
        print("Creating widgets...")  # Debugging widget creation
        self.title_label = tk.Label(self.root, text="Benny's Billiards and Sports Bar", font=("Helvetica", 16))
        self.title_label.pack(pady=20)

        self.table_label = tk.Label(self.root, text="Select a Table (1-10)", font=("Helvetica", 12))
        self.table_label.pack()

        # Frame to hold table buttons
        self.table_buttons_frame = tk.Frame(self.root)
        self.table_buttons_frame.pack(pady=10)

        # Create table buttons (1-10)
        self.table_buttons = {}
        for i in range(1, 11):
            button = tk.Button(self.table_buttons_frame, text=f"Table {i}", width=10, height=2, bg="green",
                               command=lambda i=i: self.select_table(i))
            button.grid(row=(i-1)//5, column=(i-1)%5, padx=10, pady=5)  # Grid 5 buttons per row
            self.table_buttons[i] = button

        self.table_info_frame = tk.Frame(self.root)
        self.table_info_frame.pack(pady=20)

        self.customer_name_label = tk.Label(self.table_info_frame, text="Customer Name: ")
        self.customer_name_entry = tk.Entry(self.table_info_frame)
        self.customer_name_label.grid(row=0, column=0)
        self.customer_name_entry.grid(row=0, column=1)

        self.customer_email_label = tk.Label(self.table_info_frame, text="Customer Email: ")
        self.customer_email_entry = tk.Entry(self.table_info_frame)
        self.customer_email_label.grid(row=1, column=0)
        self.customer_email_entry.grid(row=1, column=1)

        self.customer_phone_label = tk.Label(self.table_info_frame, text="Customer Phone: ")
        self.customer_phone_entry = tk.Entry(self.table_info_frame)
        self.customer_phone_label.grid(row=2, column=0)
        self.customer_phone_entry.grid(row=2, column=1)

        self.pricing_label = tk.Label(self.table_info_frame, text="Pricing: ")
        self.pricing_var = tk.StringVar(value='basic')
        self.basic_radio = tk.Radiobutton(self.table_info_frame, text="Basic ($20/hour)", variable=self.pricing_var, value="basic")
        self.premium_radio = tk.Radiobutton(self.table_info_frame, text="League ($30/hour)", variable=self.pricing_var, value="league")
        self.pricing_label.grid(row=3, column=0)
        self.basic_radio.grid(row=3, column=1, sticky=tk.W)
        self.premium_radio.grid(row=4, column=1, sticky=tk.W)

        self.start_button = tk.Button(self.table_info_frame, text="Start Rental", command=self.start_rental)
        self.start_button.grid(row=5, columnspan=2)

        self.stop_button = tk.Button(self.table_info_frame, text="Stop Rental", command=self.stop_rental, state=tk.DISABLED)
        self.stop_button.grid(row=6, columnspan=2)

    def select_table(self, table_number):
        print(f"Table {table_number} selected.")  # Debugging table selection

        # Reset the previously selected table color if not rented
        if self.selected_table is not None:
            if not self.rentals.get(self.selected_table, {}).get('active', False):
                self.table_buttons[self.selected_table].config(bg="green")

        self.selected_table = table_number

        # Change the selected table's color to gray if not actively rented
        rental = self.rentals.get(self.selected_table)
        if rental and rental['active']:
            self.table_buttons[self.selected_table].config(bg="red")  # Keep red if rented
        else:
            self.table_buttons[self.selected_table].config(bg="gray")  # Set to gray if just selected

        # Populate fields if rental exists
        if rental and rental['active']:
            self.customer_name_entry.delete(0, tk.END)
            self.customer_name_entry.insert(0, rental['customer_name'])
            self.customer_email_entry.delete(0, tk.END)
            self.customer_email_entry.insert(0, rental['customer_email'])
            self.customer_phone_entry.delete(0, tk.END)
            self.customer_phone_entry.insert(0, rental['customer_phone'])
            self.pricing_var.set(rental['price_type'])
        else:
            self.clear_table_info()

        self.table_info_frame.pack_forget()
        self.table_info_frame.pack(pady=20)

    def clear_table_info(self):
        print("Clearing table info.")  # Debugging clearing inputs
        self.customer_name_entry.delete(0, tk.END)
        self.customer_email_entry.delete(0, tk.END)
        self.customer_phone_entry.delete(0, tk.END)
        self.pricing_var.set('basic')  # Default to 'basic' pricing

    def start_rental(self):
        if self.selected_table is None:
            messagebox.showwarning("No Table Selected", "Please select a table first!")
            return

        print("Starting rental...")  
        name = self.customer_name_entry.get()
        email = self.customer_email_entry.get()
        phone = self.customer_phone_entry.get()
        price_type = self.pricing_var.get()

        if not name or not email or not phone:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        self.rentals[self.selected_table] = {
            'customer_name': name,
            'customer_email': email,
            'customer_phone': phone,
            'price_type': price_type,
            'start_time': datetime.now(),
            'price_per_hour': self.pricing[price_type],
            'active': True
        }

        # Change button color to red when rental starts
        self.table_buttons[self.selected_table].config(bg="red")

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        messagebox.showinfo("Rental Started", f"Rental for Table {self.selected_table} has started!")

    def stop_rental(self):
        print("Stopping rental...")  
        rental = self.rentals.get(self.selected_table)

        if rental and rental['active']:
            rental['end_time'] = datetime.now()
            rental['duration'] = (rental['end_time'] - rental['start_time']).total_seconds() / 3600  
            rental['total_price'] = rental['duration'] * rental['price_per_hour']
            rental['active'] = False

            # Reset the button color to gray (still selected but not rented)
            self.table_buttons[self.selected_table].config(bg="gray")

            messagebox.showinfo("Rental Stopped", f"Rental for Table {self.selected_table} stopped.\nTotal Price: ${rental['total_price']:.2f}")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.clear_table_info()
        else:
            messagebox.showwarning("No Active Rental", "No active rental for this table.")

# Create the Tkinter root window
root = tk.Tk()
print("Starting Tkinter event loop...")  # Debugging event loop
app = PoolHallApp(root)

# Run the Tkinter event loop
root.mainloop()

