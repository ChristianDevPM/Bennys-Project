import tkinter as tk                # Tkinter for the GUI
from tkinter import messagebox      # Tkinter message box for alerts and errors
from datetime import datetime       # for time handling
import pyodbc                       # for the database connection
from tkinter import PhotoImage      # to add logos
import re                           # for enforcing format restrictions

# Class to manage the pool hall application
class PoolHallApp:
    

# Starts the app and creates the window from from Tkinter
    def __init__(self, root):
        print("Initializing the application...") 
        self.root = root
        self.root.title("Cue Time Systems: Table Rental System (v1.25)")
        self.root.geometry("1000x800")
        # self.root.configure(bg="oldlace")      #set background color if we want to change it, but beware it messes with all frames unless you change them individually
        # https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html      <<<< great reference for color options
        #search the color name below for all instances and replace, then come back and change the word for reference next line
        #SEARCH COLOR NAME: oldlace
        self.pricing = {
            'standard_weekday': 3.00,
            'standard_weekend': 3.00,
            'friday_saturday_night': 5.00,
            'league': 3.00,
            'week_night_group': 15.00
        }

# Initialize rentals as a list for each table for consistency
        self.rentals = {table_number: [] for table_number in range(1, 11)}
        self.selected_table = None                      # Track the currently selected table
        self.selected_rate = tk.StringVar(value="")     # Ensure no preselection
        self.waitlist = []  # Initialize waitlist as a list
        self.create_widgets()
        self.db_connection = self.connect_to_database()

# Database connection
    def connect_to_database(self):
        try:
            connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-56QDB7K;'
                'DATABASE=bennys;'
                'Trusted_Connection=yes;'
            )
            print("Database connection established.")
            return connection
        except pyodbc.Error as e:
            print(f"Error connecting to database: {e}")
            messagebox.showerror("Database Error", "Could not connect to the database.")
            return None

# All of the photos, buttons etc.
    def create_widgets(self):
        print("Creating widgets...") 
        self.title_label = tk.Label(self.root, text="Benny's Billiards and Sports Bar", font=("Helvetica", 20))
        self.title_label.pack(pady=20)
        #background color for the title
        # self.title_label.configure(bg="oldlace")


# Benny's logo
        try:
            self.bennys_photo = PhotoImage(file="logo.png").subsample(5, 5)     # Adjust size
            self.bennys_label = tk.Label(self.root, image=self.bennys_photo)  
            self.bennys_label.place(relx=0.2, rely=0.5, anchor="center")        # Adjust position
            #background color for the logo
            # self.bennys_label.configure(bg="oldlace")  # Set the background color to match the window, use tkinter color names and remember to change ALL
        except Exception as e:
            print(f"Error loading Benny's logo: {e}")
            self.bennys_label = tk.Label(self.root, text="Logo Not Available", font=("Helvetica", 12))
            self.bennys_label.place(relx=0.2, rely=0.5, anchor="center")        # Keep consistent positioning

# CueTime logo
        try:
            self.cts_photo = PhotoImage(file="ctslogo.png").subsample(1, 1)     # Adjust size
            self.cts_label = tk.Label(self.root, image=self.cts_photo)  
            self.cts_label.place(relx=0.8, rely=0.5, anchor="center")           # Adjust position
            #background color for the logo
            # self.cts_label.configure(bg="oldlace")  # Set the background color to match the window, use tkinter color names and remember to change ALL 
        except Exception as e:
            print(f"Error loading CueTime logo: {e}")
            self.cts_label = tk.Label(self.root, text="Logo Not Available", font=("Helvetica", 12))
            self.cts_label.place(relx=0.8, rely=0.5, anchor="center")           # Keep consistent positioning


        self.table_label = tk.Label(self.root, text="Select a Table (1-10)", font=("Helvetica", 12))
        self.table_label.pack()
        #background color for the label
        # self.table_label.configure(bg="oldlace")  # Set the background color to match the window, use tkinter color names and remember to change ALL

# Frame to hold table buttons
        self.table_buttons_frame = tk.Frame(self.root)
        self.table_buttons_frame.pack(pady=10)
        #background color for the frame
        # self.table_buttons_frame.configure(bg="oldlace")  # Set the background color to match the window, use tkinter color names and remember to change ALL

# Create table buttons (1-10)
        self.table_buttons = {}
        for i in range(1, 11):
            button = tk.Button(self.table_buttons_frame, 
                               text=f"Table {i}", 
                               width=10, height=2, 
                               bg="lightblue", fg="black", 
                               font=("Helvetica", 10, "bold"),
                               command=lambda i=i: self.select_table(i))
            button.grid(row=(i-1)//5, column=(i-1)%5, padx=10, pady=5)
            self.table_buttons[i] = button
            #background color for the button
            button.configure(bg="lightblue")  # Set the background color to match the window, use tkinter color names and remember to change ALL

# Input fields for customer details, each group self explanatory
        self.customer_first_name_label = tk.Label(self.root, text="First Name:")
        self.customer_first_name_label.pack()
        self.customer_first_name_entry = tk.Entry(self.root)
        self.customer_first_name_entry.pack()
        #background color for the label
        # self.customer_first_name_label.configure(bg="oldlace")

        self.customer_last_name_label = tk.Label(self.root, text="Last Name:")
        self.customer_last_name_label.pack()
        self.customer_last_name_entry = tk.Entry(self.root)
        self.customer_last_name_entry.pack()
        #background color for the label
        # self.customer_last_name_label.configure(bg="oldlace")

        self.customer_phone_label = tk.Label(self.root, text="Phone Number:")
        self.customer_phone_label.pack()
        self.customer_phone_entry = tk.Entry(self.root)
        self.customer_phone_entry.pack()
        find_button = tk.Button(self.root, text="Player Lookup", command=self.find_customer, bg="lightblue", font=("Helvetica", 10, "bold"))
        find_button.pack(pady=5)
        #background color for the label
        # self.customer_phone_label.configure(bg="oldlace")

        self.customer_email_label = tk.Label(self.root, text="Email Address:")
        self.customer_email_label.pack()
        self.customer_email_entry = tk.Entry(self.root)
        self.customer_email_entry.pack()
        #background color for the label
        # self.customer_email_label.configure(bg="oldlace")

        self.customer_league_label = tk.Label(self.root, text="League Name (Optional):")
        self.customer_league_label.pack()
        self.customer_league_entry = tk.Entry(self.root)
        self.customer_league_entry.pack()
        #background color for the label
        # self.customer_league_label.configure(bg="oldlace")

# Radio Buttons for rate selection
        self.rate_label = tk.Label(self.root, text="Select Rate:", font=("Helvetica", 12))
        self.rate_label.pack(pady=10)
        #background color for the label
        # self.rate_label.configure(bg="oldlace")  # Set the background color to match the window, use tkinter color names and remember to change ALL

# Frame to hold the radio buttons
        self.selected_rate = tk.StringVar(value="")
        rate_frame = tk.Frame(self.root)  
        rate_frame.pack()
        #background color for the frame
        # rate_frame.configure(bg="oldlace")  # Set the background color to match the window, use tkinter color names and remember to change ALL

        self.rate_standard_weekday = tk.Radiobutton(rate_frame, text="Standard Weekday: $3.00", variable=self.selected_rate, value='1', anchor="w", command=self.debug_selected_rate)
        self.rate_standard_weekday.grid(row=0, sticky="w", padx=10)
        #background color for the label
        # self.rate_standard_weekday.configure(bg="oldlace")  # Set the background color to match the window, use tkinter color names and remember to change ALL

        self.rate_standard_weekend = tk.Radiobutton(rate_frame, text="Standard Weekend: $3.00", variable=self.selected_rate, value='2', anchor="w", command=self.debug_selected_rate)
        self.rate_standard_weekend.grid(row=1, sticky="w", padx=10)
        #background color for the label
        # self.rate_standard_weekend.configure(bg="oldlace")  # Set the background color to match the window, use tkinter color names and remember to change ALL

        self.rate_friday_saturday_night = tk.Radiobutton(rate_frame, text="Friday and Saturday Nights: $5.00", variable=self.selected_rate, value='3', anchor="w", command=self.debug_selected_rate)
        self.rate_friday_saturday_night.grid(row=2, sticky="w", padx=10)
        #background color for the label
        # self.rate_friday_saturday_night.configure(bg="oldlace")  # Set the background color to match the window, use tkinter color names and remember to change ALL

        self.rate_league = tk.Radiobutton(rate_frame, text="League: $3.00", variable=self.selected_rate, value='4', anchor="w", command=self.debug_selected_rate)
        self.rate_league.grid(row=3, sticky="w", padx=10)
        #background color for the label
        # self.rate_league.configure(bg="oldlace")  # Set the background color to match the window, use tkinter color names and remember to change ALL

        self.rate_week_night_group = tk.Radiobutton(rate_frame, text="Week Night Group: $15.00", variable=self.selected_rate, value='5', anchor="w", command=self.debug_selected_rate)
        self.rate_week_night_group.grid(row=4, sticky="w", padx=10)
        #background color for the label
        # self.rate_week_night_group.configure(bg="oldlace")  # Set the background color to match the window, use tkinter color names and remember to change ALL

        self.selected_rate.set("")  # Ensure no rate is preselected

# Start and stop buttons
        self.start_button = tk.Button(self.root, 
                                      text="Add Player", 
                                      command=self.start_rental, 
                                      state=tk.DISABLED, 
                                      bg="springgreen3", fg="black", 
                                      disabledforeground="black",
                                      font=("Helvetica", 12, "bold"),
                                      width=12, # width
                                      height=4) # height
        self.start_button.place(relx=0.25, rely=0.86, anchor="center") # position

        self.show_customer_info_button = tk.Button(self.root, 
                                                   text="Manage Players", 
                                                   command=self.show_customer_info, 
                                                   state=tk.NORMAL,
                                                   bg="dodgerblue2",          # background color
                                                   fg="black",              # text color
                                                   width=12,                # width in characters
                                                   height=4,                # height in text lines
                                                   font=("Helvetica", 12, "bold"))
        self.show_customer_info_button.place(relx=0.39, rely=0.86, anchor="center")

        self.show_waitlist_button = tk.Button(self.root, 
                                                   text="Manage Waitlist", 
                                                   command=self.show_waitlist, 
                                                   state=tk.NORMAL,
                                                   bg="navajowhite3",       # background color
                                                   fg="black",              # text color
                                                   width=12,                # width in characters
                                                   height=4,                # height in text lines
                                                   font=("Helvetica", 12, "bold"))
        self.show_waitlist_button.place(relx=0.73, rely=0.86, anchor="center")


        self.add_to_waitlist_button = tk.Button(self.root, 
                                                   text="Add to Waitlist", 
                                                   command=self.add_to_waitlist, 
                                                   state=tk.NORMAL,
                                                   bg="goldenrod",       # background color
                                                   fg="black",              # text color
                                                   width=12,                # width in characters
                                                   height=4,                # height in text lines
                                                   font=("Helvetica", 12, "bold"))
        self.add_to_waitlist_button.place(relx=0.59, rely=0.86, anchor="center")       

    def add_to_waitlist(self):
        # Get customer details
        first_name = self.customer_first_name_entry.get()
        last_name = self.customer_last_name_entry.get()
        phone = self.customer_phone_entry.get()
        email = self.customer_email_entry.get()
        league_name = self.customer_league_entry.get()

        # Validate required fields
        if not first_name or not last_name or not phone or not email:
            messagebox.showerror("Input Error", "First Name, Last Name, Phone Number, and Email Address are required!")
            return

        # Enforce formatting restrictions
        if not re.match(r"^\d{3}-\d{3}-\d{4}$", phone):
            messagebox.showerror("Input Error", "Phone number must be in the format xxx-xxx-xxxx.")
            return
        if not re.match("^[A-Za-z]+$", first_name):
            messagebox.showerror("Input Error", "First Name must contain only alphabetic characters.")
            return
        if not re.match("^[A-Za-z]+$", last_name):
            messagebox.showerror("Input Error", "Last Name must contain only alphabetic characters.")
            return
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messagebox.showerror("Input Error", "Email address must be in the format example@domain.com.")
            return

        # Validate rate selection
        selected_rate_id = self.selected_rate.get()
        if not selected_rate_id:
            messagebox.showerror("Rate Error", "Please select a rate before adding a player to the waitlist.")
            return

        # Add customer to the waitlist
        self.waitlist.append({
            "First Name": first_name,
            "Last Name": last_name,
            "Phone": phone,
            "Email": email,
            "League Name": league_name,
            "Rate ID": selected_rate_id  # Store the selected rate ID for reference
        })
        messagebox.showinfo("Waitlist", f"{first_name} {last_name} has been added to the waitlist.")
        self.clear_table_info()

    def show_waitlist(self):
        if not self.waitlist:
            messagebox.showinfo("Waitlist", "The waitlist is currently empty.")
            return

        waitlist_window = tk.Toplevel(self.root)
        waitlist_window.title("Manage Waitlist")
        waitlist_window.geometry("900x400")
        waitlist_window.attributes("-topmost", True)

        header_font = ("Helvetica", 10, "bold")
        cell_font = ("Helvetica", 10)
        headers = ["First Name", "Last Name", "Phone", "Email", "League Name", "Table Number", "Actions"]
        for col, header in enumerate(headers):
            lbl = tk.Label(waitlist_window, text=header, font=header_font, borderwidth=1, relief="solid", padx=5, pady=5)
            lbl.grid(row=0, column=col, sticky="nsew")
            waitlist_window.grid_columnconfigure(col, weight=1)

        self.waitlist_rows = {}
        for idx, customer in enumerate(self.waitlist, start=1):
            for col_idx, key in enumerate(["First Name", "Last Name", "Phone", "Email", "League Name"]):
                lbl = tk.Label(waitlist_window, text=customer[key], font=cell_font, borderwidth=1, relief="solid", padx=5, pady=5)
                lbl.grid(row=idx, column=col_idx, sticky="nsew")

            # Add an editable entry for the table number
            table_number_entry = tk.Entry(waitlist_window, font=cell_font, borderwidth=1, relief="solid")
            table_number_entry.grid(row=idx, column=len(headers) - 2, sticky="nsew")
            self.waitlist_rows[idx - 1] = {"customer": customer, "table_entry": table_number_entry}

            assign_button = tk.Button(waitlist_window, text="Assign to Table", font=cell_font,
                                       command=lambda idx=idx-1: self.assign_to_table(idx, waitlist_window))
            assign_button.grid(row=idx, column=len(headers) - 1, sticky="nsew")

    def assign_to_table(self, waitlist_index, parent_window):
        row_data = self.waitlist_rows.get(waitlist_index)
        if not row_data:
            messagebox.showerror("Error", "Invalid waitlist entry.")
            return

        customer = row_data["customer"]
        table_number = row_data["table_entry"].get()

        # Validate the table number
        if not table_number.isdigit() or int(table_number) not in self.table_buttons:
            messagebox.showerror("Input Error", "Please enter a valid table number (1-10).")
            return

        table_number = int(table_number)
        if any(r.get('active', False) for r in self.rentals.get(table_number, [])):
            messagebox.showerror("Table Occupied", f"Table {table_number} is currently occupied.")
            return

        # Remove customer from the waitlist
        self.waitlist.pop(waitlist_index)

        # Start the rental process
        self.selected_table = table_number
        self.customer_first_name_entry.insert(0, customer["First Name"])
        self.customer_last_name_entry.insert(0, customer["Last Name"])
        self.customer_phone_entry.insert(0, customer["Phone"])
        self.customer_email_entry.insert(0, customer["Email"])
        self.customer_league_entry.insert(0, customer["League Name"])
        parent_window.destroy()
        self.start_rental()

# For showing the guest's info
    def show_customer_info(self):
        if self.selected_table is None:
            messagebox.showwarning("No Table Selected", "Please select a table first!")
            return
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                SELECT r.SessionID, c.CustomerID, c.FirstName, c.LastName, c.PhoneNumber, c.EmailAddress, c.LeagueName,
                       r.TableID, r.RentalStart, r.RentalEnd, r.TotalPrice, r.RateID
                FROM POOLRENTAL r
                JOIN CUSTOMER c ON r.CustomerID = c.CustomerID
                WHERE r.TableID = ? AND r.RentalEnd IS NULL
                ORDER BY r.RentalStart DESC
            """, (self.selected_table,))
            rows = cursor.fetchall()
            if rows:
                info_window = tk.Toplevel(self.root)
                info_window.title(f"Customer Info - Table {self.selected_table}")
                info_window.geometry("1300x400")
                info_window.attributes("-topmost", True)
                
                header_font = ("Helvetica", 10, "bold")
                cell_font = ("Helvetica", 10)
                headers = ["Actions", "Customer ID", "First Name", "Last Name", "Phone Number", "Email Address",
                           "League Name", "Table Number", "Time Played (minutes)", "Total Price"]
                for col, header in enumerate(headers):
                    lbl = tk.Label(info_window, text=header, font=header_font, borderwidth=1, relief="solid", padx=5, pady=5)
                    lbl.grid(row=0, column=col, sticky="nsew")
                    info_window.grid_columnconfigure(col, weight=1)
                
                self.info_rows = {}
                
                def make_edit_callback(session_id):
                    def enable_edit():
                        row_widgets = self.info_rows[session_id]
                        # Allows for editing only these fields, below:
                        for key in ["First Name", "Last Name", "Phone Number", "Email Address", "League Name", "Table Number"]:
                            row_widgets['cells'][key].destroy()
                            entry = tk.Entry(info_window, font=cell_font, borderwidth=1, relief="solid")
                            entry.insert(0, row_widgets['data'][key])
                            entry.grid(row=row_widgets['row'], column=headers.index(key), sticky="nsew")
                            row_widgets['cells'][key] = entry
                        # Restricts the editing of time played and total price
                        row_widgets['edit_btn'].config(state=tk.DISABLED)
                        row_widgets['confirm_btn'].config(state=tk.NORMAL)
                    return enable_edit

                def make_confirm_callback(session_id):
                    def confirm_update():
                        row_widgets = self.info_rows[session_id]
                        original_table = row_widgets['data']["Table Number"]
                        updated = {}
                        for key in ["First Name", "Last Name", "Phone Number", "Email Address", "League Name", "Table Number"]:
                            updated[key] = row_widgets['cells'][key].get()
                        try:
                            update_cursor = self.db_connection.cursor()
                            # Update CUSTOMER info
                            update_cursor.execute("""
                                UPDATE CUSTOMER
                                SET FirstName = ?, LastName = ?, PhoneNumber = ?, EmailAddress = ?, LeagueName = ?
                                WHERE CustomerID = ?
                            """, (updated["First Name"], updated["Last Name"], updated["Phone Number"],
                                  updated["Email Address"], updated["League Name"], row_widgets['data']["Customer ID"]))
                            self.db_connection.commit()
                            # Also update TableID in POOLRENTAL if changed
                            if updated["Table Number"] != str(original_table):
                                update_cursor.execute("""
                                    UPDATE POOLRENTAL
                                    SET TableID = ?
                                    WHERE SessionID = ?
                                """, (updated["Table Number"], session_id))
                                self.db_connection.commit()
                                if isinstance(self.rentals.get(original_table), list):
                                    self.rentals[original_table] = [r for r in self.rentals[original_table] if r.get('customer_name') != row_widgets['data']["Customer ID"]]
                                # Put a guest on new table:
                                if self.rentals.get(updated["Table Number"]):
                                    if isinstance(self.rentals[updated["Table Number"]], list):
                                        self.rentals[updated["Table Number"]].append(row_widgets['data'])
                                else:
                                    self.rentals[updated["Table Number"]] = [row_widgets['data']]
                            for key in ["First Name", "Last Name", "Phone Number", "Email Address", "League Name", "Table Number"]:
                                row_widgets['cells'][key].destroy()
                                lbl = tk.Label(info_window, text=updated[key], font=cell_font, borderwidth=1, relief="solid", padx=5, pady=5)
                                lbl.grid(row=row_widgets['row'], column=headers.index(key), sticky="nsew")
                                row_widgets['cells'][key] = lbl
                                row_widgets['data'][key] = updated[key]
                            row_widgets['edit_btn'].config(state=tk.NORMAL)
                            row_widgets['confirm_btn'].config(state=tk.DISABLED)
                            self.update_table_buttons()  # update table buttons after editing table number
                        except Exception as ex:
                            messagebox.showerror("Update Error", f"Failed to update customer info: {ex}")
                    return confirm_update

                def make_stop_callback(session_id):
                    def stop_single():
                        self.stop_individual_rental(session_id, info_window)
                    return stop_single
                
                for idx, row in enumerate(rows[:10], start=1):
                    session_id = row[0]
                    rental_start = row[8] 
                    rental_end = row[9]    
                    if rental_start and rental_end:
                        from datetime import datetime, date
                        dt_start = datetime.combine(date.today(), rental_start)
                        dt_end = datetime.combine(date.today(), rental_end)
                        delta = (dt_end - dt_start).total_seconds() / 60
                        time_played = f"{delta:.0f}"
                    else:
                        time_played = ""
                    total_price = "" if row[10] is None else f"{row[10]:.2f}"
                    data = {
                        "Customer ID": row[1],
                        "First Name": row[2],
                        "Last Name": row[3],
                        "Phone Number": row[4],
                        "Email Address": row[5],
                        "League Name": row[6],
                        "Table Number": row[7],
                        "Time Played (minutes)": time_played,
                        "Total Price": total_price,
                        "RateID": row[11]      
                    }
                    row_widgets = {"data": data, "cells": {}}
                    action_frame = tk.Frame(info_window)
                    action_frame.grid(row=idx, column=0, sticky="nsew")
                    edit_btn = tk.Button(action_frame, text="Edit", font=cell_font, command=make_edit_callback(session_id))
                    edit_btn.pack(side="left", padx=2)
                    confirm_btn = tk.Button(action_frame, text="Confirm", font=cell_font, command=make_confirm_callback(session_id), state=tk.DISABLED)
                    confirm_btn.pack(side="left", padx=2)
                    stop_btn = tk.Button(action_frame, text="Stop Rental", font=cell_font, command=make_stop_callback(session_id))
                    stop_btn.pack(side="left", padx=2)
                    row_widgets['edit_btn'] = edit_btn
                    row_widgets['confirm_btn'] = confirm_btn
                    for col_idx, key in enumerate(["Customer ID", "First Name", "Last Name", "Phone Number", "Email Address", "League Name", "Table Number", "Time Played (minutes)", "Total Price"], start=1):
                        lbl = tk.Label(info_window, text=data[key], font=cell_font, borderwidth=1, relief="solid", padx=5, pady=5)
                        lbl.grid(row=idx, column=col_idx, sticky="nsew")
                        row_widgets['cells'][key] = lbl
                    row_widgets['data']["RentalStart"] = rental_start
                    self.info_rows[session_id] = {"row": idx, **row_widgets}
            else:
                messagebox.showwarning("No Customer Info", "No customer information found for this table.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error retrieving customer info: {e}")
        finally:
            cursor.close()

    def stop_individual_rental(self, session_id, parent_window):
        try:
            cursor = self.db_connection.cursor()
            now = datetime.now()
            # Update the end time in the database
            cursor.execute("""
                UPDATE POOLRENTAL
                SET RentalEnd = ?
                WHERE SessionID = ? AND RentalEnd IS NULL
            """, (now.time(), session_id))
            self.db_connection.commit()

            # Retrieve the rental start time from the database
            cursor.execute("SELECT RentalStart FROM POOLRENTAL WHERE SessionID = ?", (session_id,))
            rental_start_row = cursor.fetchone()
            if not rental_start_row:
                messagebox.showerror("Error", "Could not retrieve rental start time.")
                return

            rental_start_time = rental_start_row[0] 
            rental_start = datetime.combine(now.date(), rental_start_time)  # Combine with today's date

            # Calculate the rental duration and round up to the next hour
            rental_duration_seconds = (now - rental_start).total_seconds()
            rental_hours = int(rental_duration_seconds // 3600) + (1 if rental_duration_seconds % 3600 > 0 else 0)

            # Retrieve the hourly rate from the database
            cursor.execute("""
                SELECT r.Rate
                FROM POOLRENTAL p
                JOIN Rates r ON p.RateID = r.RateID
                WHERE p.SessionID = ?
            """, (session_id,))
            rate_row = cursor.fetchone()
            if not rate_row:
                messagebox.showerror("Error", "Could not retrieve hourly rate.")
                return

            hourly_rate = float(rate_row[0])
            total_price = rental_hours * hourly_rate

            # Update the total price in the database
            cursor.execute("""
                UPDATE POOLRENTAL
                SET TotalPrice = ?
                WHERE SessionID = ?
            """, (total_price, session_id))
            self.db_connection.commit()

            messagebox.showinfo("Rental Stopped", f"Session {session_id} stopped.\nTotal Price: ${total_price:.2f}", parent=parent_window)

            
            cursor.execute("SELECT TotalPrice FROM POOLRENTAL WHERE SessionID = ?", (session_id,))
            db_total = cursor.fetchone()
            if db_total:
                db_total_price = f"{db_total[0]:.2f}"
            else:
                db_total_price = "0.00"

            headers = ["Actions", "Customer ID", "First Name", "Last Name", "Phone Number", "Email Address",
                       "League Name", "Table Number", "Time Played (minutes)", "Total Price"]
            row_widgets = self.info_rows.get(session_id)
            if row_widgets:
                time_played = f"{int(rental_duration_seconds // 60)}"
                tp_lbl = tk.Label(parent_window, text=time_played, font=("Helvetica", 10, "bold"),
                                  borderwidth=1, relief="solid", padx=5, pady=5)
                tp_lbl.grid(row=row_widgets['row'], column=headers.index("Time Played (minutes)"), sticky="nsew")
                row_widgets['cells']["Time Played (minutes)"] = tp_lbl
                price_lbl = tk.Label(parent_window, text=db_total_price, font=("Helvetica", 10, "bold"),
                                     borderwidth=1, relief="solid", padx=5, pady=5)
                price_lbl.grid(row=row_widgets['row'], column=headers.index("Total Price"), sticky="nsew")
                row_widgets['cells']["Total Price"] = price_lbl
                row_widgets['data']["Total Price"] = db_total_price
                row_widgets['edit_btn'].config(state=tk.DISABLED)
                row_widgets['confirm_btn'].config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not stop session {session_id}: {e}")
        finally:
            cursor.close()

# Debugging to make sure rates work right
    def debug_selected_rate(self):
        print(f"[DEBUG] Current selected rate: {self.selected_rate.get()}")  

 
 # Table selection and button color config
    def select_table(self, table_number):
        # Update the selected table
        self.selected_table = table_number
        print(f"Table {self.selected_table} selected.")

# Clear the entry fields
        self.clear_table_info()
        self.update_table_buttons()
        self.start_button.config(state=tk.NORMAL)
        self.show_customer_info_button.config(state=tk.NORMAL)

# Clears the customer input fields when a table is selected  
    def clear_table_info(self):
        print("Clearing table info.") 
        self.customer_first_name_entry.delete(0, tk.END)
        self.customer_last_name_entry.delete(0, tk.END)
        self.customer_phone_entry.delete(0, tk.END)
        self.customer_email_entry.delete(0, tk.END)
        self.customer_league_entry.delete(0, tk.END)

# Stops user from proceeding if they don't select a table first
    def start_rental(self):
        # Check if a table is selected
        if self.selected_table is None:
            messagebox.showwarning("No Table Selected", "Please select a table first!")
            return

        # Get customer details
        first_name = self.customer_first_name_entry.get()
        last_name = self.customer_last_name_entry.get()
        phone = self.customer_phone_entry.get()
        email = self.customer_email_entry.get()
        league_name = self.customer_league_entry.get()

        # Validate required fields
        if not first_name or not last_name or not phone or not email:
            messagebox.showerror("Input Error", "First Name, Last Name, Phone Number, and Email Address are required!")
            return

        # Enforce formatting restrictions
        if not re.match(r"^\d{3}-\d{3}-\d{4}$", phone):
            messagebox.showerror("Input Error", "Phone number must be in the format xxx-xxx-xxxx.")
            return
        if not re.match("^[A-Za-z]+$", first_name):
            messagebox.showerror("Input Error", "First Name must contain only alphabetic characters.")
            return
        if not re.match("^[A-Za-z]+$", last_name):
            messagebox.showerror("Input Error", "Last Name must contain only alphabetic characters.")
            return
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messagebox.showerror("Input Error", "Email address must be in the format example@domain.com.")
            return

        # If user did not use lookup, verify that this phone number is not already in use
        if not (hasattr(self, "existing_customer_id") and self.existing_customer_id):
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("SELECT CustomerID FROM CUSTOMER WHERE PhoneNumber = ?", (phone,))
                row = cursor.fetchone()
                if row:
                    messagebox.showerror("Duplicate Customer",
                        "A customer with this phone number already exists. Please use the Find Customer button to proceed.")
                    return
                cursor.close()
            except Exception as e:
                messagebox.showerror("Database Error", f"Error checking for existing customer: {e}")
                return

        # Get the selected rate
        selected_rate_id = self.selected_rate.get()
        if not selected_rate_id:
            messagebox.showerror("Rate Error", "Please select a rate.")
            return
        try:
            selected_rate_id = int(selected_rate_id)
        except ValueError:
            messagebox.showerror("Rate Error", "Invalid rate selected.")
            return

        # Query the database to get the rate in dollars for the selected RateID
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT Rate FROM Rates WHERE RateID = ?", (selected_rate_id,))
            rate_row = cursor.fetchone()
            if not rate_row:
                messagebox.showerror("Rate Error", "Selected rate not found in the database.")
                return
            print(f"[DEBUG] Fetched raw rate for RateID {selected_rate_id}: {rate_row[0]}")
            price_per_hour = float(rate_row[0])
            print(f"[DEBUG] Converted price_per_hour: {price_per_hour}")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error retrieving rate from the database: {e}")
            return

        # Determine customer_id or use existing if lookup was done
        if hasattr(self, "existing_customer_id") and self.existing_customer_id:
            customer_id = self.existing_customer_id
        else:
            customer_id = None
            try:
                cursor = self.db_connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO CUSTOMER (FirstName, LastName, PhoneNumber, EmailAddress, LeagueName)
                    OUTPUT INSERTED.CustomerID
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    first_name, last_name, phone, email, league_name
                )
                customer_id = cursor.fetchone()[0]
                self.db_connection.commit()
            except pyodbc.Error as e:
                messagebox.showerror("Database Error", "Could not insert customer data into the database.")
                return

        # Insert rental data into the database
        try:
            cursor = self.db_connection.cursor()
            query = """
                INSERT INTO POOLRENTAL (RateID, CustomerID, TableID, RentalDate, RentalStart, RentalEnd, TotalPlayers)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                selected_rate_id,
                customer_id,
                self.selected_table,
                datetime.now().date(),
                datetime.now().time(),
                None,
                1
            )
            cursor.execute(query, params)
            self.db_connection.commit()
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", "Could not insert rental data into the database.")
            return

        # Mark the rental as active, update UI, and reset lookup
        rental_record = {
            'active': True,
            'start_time': datetime.now(),
            'end_time': None,
            'price_per_hour': price_per_hour,
            'total_price': 0,
            'customer_name': f"{first_name} {last_name}"
        }
        if self.selected_table in self.rentals and isinstance(self.rentals[self.selected_table], list):
            self.rentals[self.selected_table].append(rental_record)
        else:
            self.rentals[self.selected_table] = [rental_record]
        self.table_buttons[self.selected_table].config(bg="green")
        self.existing_customer_id = None
        self.show_customer_info_button.config(state=tk.NORMAL)
        self.clear_table_info()
        self.update_table_buttons()  

# Stops the rental and updates the database
    def stop_rental(self):
        # Ensure the selected table is valid
        if self.selected_table is None:
            messagebox.showerror("Error", "No table selected!")
            return

        # Get active rental record from the list for the selected table
        rentals_list = self.rentals.get(self.selected_table, [])
        active_rental = None
        for rental in rentals_list:
            if rental.get('active', False):
                active_rental = rental
                break
        if active_rental is None:
            messagebox.showerror("Stop Rental Error", "No active rental found for the selected table.")
            return

        # Set the end time for the active rental record
        active_rental['end_time'] = datetime.now()
        rental_duration_seconds = (active_rental['end_time'] - active_rental['start_time']).total_seconds()
        rental_hours = int(rental_duration_seconds // 3600) + (1 if rental_duration_seconds % 3600 > 0 else 0)

        # verify calculations
        print(f"[DEBUG] Rental duration in seconds: {rental_duration_seconds}")
        print(f"[DEBUG] Rental duration in hours (rounded up): {rental_hours}")

        # Uses thr stored hourly rate from rental start
        hourly_rate = active_rental['price_per_hour']
        total_price = rental_hours * hourly_rate
        active_rental['total_price'] = total_price
        active_rental['active'] = False

        print(f"[DEBUG] Hourly rate: ${hourly_rate}")
        print(f"[DEBUG] Total price: ${total_price}")

        # Update the rental in the database
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                update_query = """
                    UPDATE POOLRENTAL
                    SET RentalEnd = ?, TotalPrice = ?
                    WHERE TableID = ? AND RentalEnd IS NULL
                """
                rental_end_time = active_rental['end_time'].time()
                cursor.execute(update_query, (rental_end_time, total_price, self.selected_table))
                self.db_connection.commit()
                print(f"Rental for Table {self.selected_table} updated in database with end time {rental_end_time} and total price ${total_price}.")
            except pyodbc.Error as e:
                print(f"[ERROR] Error updating rental end time: {e}")
                messagebox.showerror("Database Error", "Could not update rental end time in the database.")
                return

        # button styling for selection and deselection and rented, etc.
        self.table_buttons[self.selected_table].config(bg="gray")
        messagebox.showinfo("Rental Stopped", 
            f"The rental for {active_rental['customer_name']} has ended.\nTotal time played is {rental_hours} hour(s).\nTotal Price is ${total_price:.2f}", 
            parent=self.root)
        self.clear_table_info()
        self.update_table_buttons() 

# Clear cache for active rentals
    def clear_active_rental_cache(self):
        print("Clearing active rental cache before exit...")
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                for table, rental in self.rentals.items():
                    if isinstance(rental, list):
                        for rec in rental:
                            if rec.get('active', False):
                                now = datetime.now().time()
                                cursor.execute("""
                                    UPDATE POOLRENTAL
                                    SET RentalEnd = ?, TotalPrice = ?
                                    WHERE TableID = ? AND RentalEnd IS NULL
                                """, (now, 0, table))
                    elif isinstance(rental, dict):
                        if rental.get('active', False):
                            now = datetime.now().time()
                            cursor.execute("""
                                UPDATE POOLRENTAL
                                SET RentalEnd = ?, TotalPrice = ?
                                WHERE TableID = ? AND RentalEnd IS NULL
                            """, (now, 0, table))
                self.db_connection.commit()
            except Exception as e:
                print(f"Error clearing active rentals from DB: {e}")
        for table in self.rentals:
            self.rentals[table] = {'active': False, 'start_time': None, 'end_time': None, 'price_per_hour': 0, 'total_price': 0}
    def on_exit(self):
        print("Exiting app: clearing active rentals and closing DB connection...")
        self.clear_active_rental_cache()
        self.close_database_connection()
        self.root.destroy()

# Close the database connection when the application is closed
    def close_database_connection(self):
        if self.db_connection:
            self.db_connection.close()
            print("Database connection closed.")
    def find_customer(self):
        phone = self.customer_phone_entry.get()
        # Phone number formatting validation..
        if not re.match(r"^\d{3}-\d{3}-\d{4}$", phone):
            messagebox.showerror("Input Error", "Phone number must be in the format xxx-xxx-xxxx.")
            return
        try:
            cursor = self.db_connection.cursor()
            # Checks CustomerID from DB so we can avoid duplicates
            query = "SELECT CustomerID, FirstName, LastName, EmailAddress, LeagueName FROM CUSTOMER WHERE PhoneNumber = ?"
            cursor.execute(query, (phone,))
            row = cursor.fetchone()
            if row:
                self.existing_customer_id = row[0]
                self.customer_first_name_entry.delete(0, tk.END)
                self.customer_first_name_entry.insert(0, str(row[1]))
                self.customer_last_name_entry.delete(0, tk.END)
                self.customer_last_name_entry.insert(0, str(row[2]))
                self.customer_email_entry.delete(0, tk.END)
                self.customer_email_entry.insert(0, str(row[3]))
                self.customer_league_entry.delete(0, tk.END)
                self.customer_league_entry.insert(0, str(row[4]))
            else:
                messagebox.showinfo("Customer Not Found", "Customer Does Not Exist Yet")
                self.existing_customer_id = None
            cursor.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error retrieving customer info: {e}")

    def update_table_buttons(self):
        for table, button in self.table_buttons.items():
            if table == self.selected_table:
                rental_entries = self.rentals.get(table, [])
                active = any(r.get('active', False) for r in rental_entries)
                if active:
                    button.config(bg="dodgerblue2", fg="black", font=("Helvetica", 10, "normal"))
                else:
                    button.config(bg="dodgerblue2", fg="black", font=("Helvetica", 10, "normal"))
            else:
                # Button configs to get colors working right
                button.config(bg="lightblue", fg="black", font=("Helvetica", 10, "bold"))

# Tkinter root window
root = tk.Tk()
print("Starting Tkinter event loop...") 
app = PoolHallApp(root)
# kills the manage player window when the main window is closed
root.protocol("WM_DELETE_WINDOW", app.on_exit)

# Tkinter event loop
root.mainloop()
