from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

currency_menu = ["USD", "AED", "SAR"]
category_menu = ["Life Expenses", "Electricity", "Gas", "Rental", "Grocery", "Savings", "Education", "Charity"]
payment_menu = ["Cash", "Credit Card", "Paypal"]
menus = [currency_menu, category_menu, payment_menu]

label_names= ["Amount", "Currency", "Category", "Payment Method", "Date"]

def create_label(frame, label_name, relief=FLAT):
    return Label(frame, text=label_name, relief=relief)

def create_menu_variable(entry_menu):
    return StringVar(window, value=entry_menu[0])

def create_combobox(menu_var, menu_list):
    return ttk.Combobox(entries_frame, textvariable=menu_var, values=menu_list, state="readonly")

def get_amount():
    # Get the amount entered and check if it's a valid float
    try:
        return float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered. Please enter a valid number.")
        return None

def get_date():
    date_str = date_entry.get()
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please enter a date in YYYY-MM-DD format.")
        return None

def add_expense():
    amount = get_amount()
    if (amount is None):
        return
    currency = menus_variables[0].get()
    category = menus_variables[1].get()
    payment_method = menus_variables[2].get()
    date = get_date()
    if (date is None):
        return
        
    # You can perform further processing with the obtained data, like saving it to a database or file.
    print("Amount:", amount)
    print("Currency:", currency)
    print("Category:", category)
    print("Payment Method:", payment_method)
    print("Date:", date)

def display_widgets(widget, row, col, padx=0, pady=0, width=None):
    widget.grid(row=row, column=col, padx=padx, pady=pady, sticky="ew")
    if width is not None:
        widget.config(width=width)

window = Tk()
window.title("Expense Tracker")

################ Entries Frame ################
entries_frame = Frame(window)

## create labels and entries
entry_labels = [create_label(entries_frame, name) for name in label_names]

amount_entry = Entry(entries_frame, width=20)
menus_variables = [create_menu_variable(menu_list) for menu_list in menus]
menus_combobox = [create_combobox(menu_var, menu_list) 
                      for menu_var, menu_list in zip(menus_variables, menus)]
date_entry = Entry(entries_frame, width=20)
date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))               # Default to today's date
entry_widgets = [amount_entry] + menus_combobox + [date_entry]

add_expense_button = Button(entries_frame, text="Add Expense", command=add_expense, width=20)

padx_label = (50, 100) 
padx_entry = (150, 5) 
pady_widgets = 5

# disaply entries frame layout
entries_frame.grid(row=0, column=0)
for i, (entry_label, widget_entry) in enumerate(zip(entry_labels, entry_widgets), start=0):
    display_widgets(entry_label, i, 0, padx=padx_label, pady=pady_widgets)
    display_widgets(widget_entry, i, 1, padx=padx_entry, pady=pady_widgets, width=20)
add_expense_button.grid(row=len(entry_labels), column=1, padx=padx_entry, pady=5, sticky="ew")
add_expense_button.config(width=20)


################ header frame ################
headers_frame = Frame(window)
header_labels = [create_label(headers_frame, name, relief=GROOVE) for name in label_names]

headers_frame.grid(row=1, column=0)
for i, header_label in enumerate(header_labels):
    display_widgets(header_label, 0, i, width=20)

window.mainloop()
