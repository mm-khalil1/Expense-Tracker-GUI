from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import requests

# Load API key from file
with open('APILayer_API_Key.env', 'r') as file:
    api_key = file.read()
headers = {"apikey": api_key}

def fetch_currencies_list():
    """
    Fetches the list of currencies from the API.

    Returns:
        list: A list of currency codes.
    """
    currencies_list_url = "https://api.apilayer.com/currency_data/list"

    try:
        response = requests.request("GET", currencies_list_url, headers=headers)
        status_code = response.status_code

        if status_code == 200:
            data = response.json()
            currencies = data.get("currencies", {})
            return list(currencies.keys())
        else:
            messagebox.showerror("Error", f"{status_code}. Unable to fetch currencies list.")
            return []
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"{e}. Unable to make the API request to fetch currencies list.")
        return None

def currency_converter(amount, base):
    """
    Converts an amount from one currency to another.

    Args:
        amount (float): The amount to be converted.
        base (str): The currency code of the base amount.

    Returns:
        float: The converted amount.
    """
    target = "USD"
    if base.upper() == target:
        return amount

    converter_url = f"https://api.apilayer.com/fixer/convert?to={target}&from={base}&amount={amount}"
    
    try:
        response = requests.request("GET", converter_url, headers=headers)    # Make the API request
        status_code = response.status_code          # Get the HTTP status code from the response

        if status_code == 200:
            return response.json()['result']
        else:
            messagebox.showerror("Error", f"{status_code}. Unable to fetch total amount conversion rates.")
            return None

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"{e}. Unable to make the API request to convert total amount.")
        return None

def create_label(frame, label_text, relief=FLAT):
    """
    Creates a Label widget.

    Args:
        frame (Tkinter.Frame): The frame to which the label will be added.
        label_text (str): The text to be displayed on the label.
        relief (str): The relief style of the label (default is FLAT).

    Returns:
        Tkinter.Label: The created Label widget.
    """
    return Label(frame, text=label_text, relief=relief)

def create_menu_variable(entry_menu):
    """
    Creates a Tkinter StringVar for a Combobox.

    Args:
        entry_menu (list): A list of menu items.

    Returns:
        Tkinter.StringVar: The created StringVar.
    """
    return StringVar(window, value=entry_menu[0])

def create_combobox(menu_var, menu_list):
    """
    Creates a Combobox widget.

    Args:
        menu_var (Tkinter.StringVar): The StringVar to be associated with the Combobox.
        menu_list (list): A list of menu items.

    Returns:
        ttk.Combobox: The created Combobox widget.
    """
    return ttk.Combobox(entries_frame, textvariable=menu_var, values=menu_list, state="readonly")

def display_widgets(widget, row, col, padx=0, pady=0, width=20, sticky="ew", bg=None):
    """
    Displays a widget in a specific grid position.

    Args:
        widget: The widget to be displayed.
        row (int): The row index.
        col (int): The column index.
        padx (int): Padding in the x-direction (default is 0).
        pady (int): Padding in the y-direction (default is 0).
        width (int): Width of the widget (default is 20).
        sticky (str): Alignment of the widget within its grid cell (default is "ew").
        bg (str): Background color of the widget (default is None).
    """
    widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
    widget.config(width=width)
    if bg is not None:
        widget.config(bg=bg)

def get_amount():
    """
    Retrieves the amount entered by the user.

    Returns:
        float or None: The entered amount if valid, else None.
    """
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            messagebox.showerror("Error", "Amount cannot be negative. Please enter a non-negative number.")
            return None
        return amount
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered. Please enter a valid number.")
        return None

def get_date():
    """
    Retrieves the date entered by the user.

    Returns:
        str or None: The entered date if valid, else None.
    """
    date_str = date_entry.get()
    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        if parsed_date <= datetime.now():           # Check if parsed date is not after today
            return parsed_date.strftime("%Y-%m-%d") # return in the form YYYY-mm-dd
        else:
            messagebox.showerror("Error", "Date cannot be in the future.")
            return None
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please enter a date in YYYY-MM-DD format.")
        return None
    
def add_expense():
    """
    Adds an expense to the data frame.
    """
    amount = get_amount()
    if (amount is None):
        return
    currency = menus_variables[0].get()
    category = menus_variables[1].get()
    payment_method = menus_variables[2].get()
    date = get_date()
    if (date is None):
        return
    
    append_expense(amount, currency, category, payment_method, date)

def append_expense(amount, currency, category, payment_method, date):
    """
    Appends expense data to the data frame.

    Args:
        amount (float): The amount of the expense.
        currency (str): The currency code of the expense.
        category (str): The category of the expense.
        payment_method (str): The payment method used for the expense.
        date (str): The date of the expense.
    """
    global total_amount
    
    amount_data.append(amount)
    currency_data.append(currency)
    category_data.append(category)
    payment_method_data.append(payment_method)
    date_data.append(date)

    data_values = [create_label(data_frame, name) 
                   for name in [amount, currency, category, payment_method, date]]
    
    display_data(data_values)

    canvas.config(scrollregion=canvas.bbox("all"))

    total_amount += currency_converter(amount, currency)
    total_amount_value_label.config(text="{:.2f}".format(total_amount))

def display_data(data_values):
    """
    Displays expense data in the data frame.

    Args:
        data_values (list): A list of expense data.
    """
    change_previous_data_bg(data_frame, "white")        

    for i, data in enumerate(data_values):
        display_widgets(data, len(amount_data)-1, i, pady=5, sticky="w", bg="yellow")
    
def change_previous_data_bg(frame, new_bg_color):
    """
    Changes the background color of previously displayed data.

    Args:
        frame (Tkinter.Frame): The frame containing the data.
        new_bg_color (str): The new background color.
    """
    for child in frame.winfo_children():
        if isinstance(child, Label):
            child.config(bg=new_bg_color)

############### Initializing GUI ##############

# currency_menu = fetch_currencies_list()
currency_menu = ['USD', 'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BWP', 'BYN', 'BYR', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF', 'CLP', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LTL', 'LVL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD', 'STD', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VEF', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMK', 'ZMW', 'ZWL']
category_menu = ["Life Expenses", "Electricity", "Gas", "Rental", "Grocery", "Savings", "Education", "Charity"]
payment_menu = ["Cash", "Credit Card", "Paypal"]
menus = [currency_menu, category_menu, payment_menu]

label_names= ["Amount", "Currency", "Category", "Payment Method", "Date"]

window = Tk()
window.title("Expense Tracker")

################ Entries Frame ################
entries_frame = Frame(window)

# create labels and entries
entry_labels = [create_label(entries_frame, name) for name in label_names]

amount_entry = Entry(entries_frame)
menus_variables = [create_menu_variable(menu_list) for menu_list in menus]
menus_combobox = [create_combobox(menu_var, menu_list) 
                      for menu_var, menu_list in zip(menus_variables, menus)]
date_entry = Entry(entries_frame)
date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))               # Default to today's date
entry_widgets = [amount_entry] + menus_combobox + [date_entry]

add_expense_button = Button(entries_frame, text="Add Expense", command=add_expense)

padx_label = (5, 100) 
padx_entry = (100, 5) 

# disaply entries frame layout
entries_frame.pack()
for i, (entry_label, widget_entry) in enumerate(zip(entry_labels, entry_widgets), start=0):
    display_widgets(entry_label, i, 0, padx=padx_label, pady=5)
    display_widgets(widget_entry, i, 1, padx=padx_entry, pady=5)
display_widgets(add_expense_button, len(entry_labels), 1, padx=padx_entry, pady=5)

################ header frame ################
headers_frame = Frame(window)
header_labels = [create_label(headers_frame, name, relief=GROOVE) for name in label_names]

headers_frame.pack()
for i, header_label in enumerate(header_labels):
    display_widgets(header_label, 0, i)

################ Data frame ################
data_outer_frame = Frame(window)
canvas = Canvas(data_outer_frame, background="white", width=730, height=190)
canvas.pack(side=LEFT, fill=Y, expand=True)
scrollbar = Scrollbar(data_outer_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)

data_frame = Frame(canvas, background="white")
canvas.create_window((0, 0), window=data_frame, anchor='nw')

# data_frame = Frame(window, background="white", width=730, height=200)

amount_data = []
currency_data = []
category_data = []
payment_method_data = []
date_data = []

data_outer_frame.pack(fill=BOTH, expand=True)
# data_frame.grid(row=2, column=0)

################ Total Amount Frame ################
total_amount_frame = Frame(window)

total_amount = 0

total_amount_label = create_label(total_amount_frame, "Total Amount: ")
total_amount_value_label = create_label(total_amount_frame, total_amount)
currency_unit_label = create_label(total_amount_frame, " USD")

total_amount_frame.pack(side=BOTTOM)
display_widgets(total_amount_label, 0, 0, pady=5, width=0, sticky='w', bg=None)
display_widgets(total_amount_value_label, 0, 1, pady=5, width=0, sticky='w', bg=None)
display_widgets(currency_unit_label, 0, 2, pady=5, width=0, sticky='w', bg=None)


window.mainloop()
