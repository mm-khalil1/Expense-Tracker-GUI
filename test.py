import tkinter as tk

# Define options for each category
gbp_options = ["£10", "£20", "£50", "£100"]
savings_options = ["Basic Savings", "High-Yield Savings"]
paypal_options = ["Send Money", "Request Money"]

# Create the main window
root = tk.Tk()
root.title("Option Menu Example")

# Create variables to store selected options
selected_gbp = tk.StringVar()
selected_savings = tk.StringVar()
selected_paypal = tk.StringVar()

# Function to handle option selection (example, update label)
def update_selection():
  selected_text = f"Selected GBP: {selected_gbp.get()}\nSelected Savings: {selected_savings.get()}\nSelected PayPal: {selected_paypal.get()}"
  selection_label.config(text=selected_text)

# Create a label to display the selected options
selection_label = tk.Label(root)
selection_label.pack()

# Style customization for the option menus

# Create the GBP option menu (apply styles)
gbp_menu = tk.OptionMenu(root, selected_gbp, *gbp_options)
gbp_menu.pack()

# Create the Savings option menu (apply styles)
savings_menu = tk.OptionMenu(root, selected_savings, *savings_options)
savings_menu.pack()

# Create the PayPal option menu (apply styles)
paypal_menu = tk.OptionMenu(root, selected_paypal, *paypal_options)
paypal_menu.pack()
# Button to trigger the update function (optional)
# update_button = tk.Button(root, text="Update Selection", command=update_selection)
# update_button.pack()
gbp_menu.configure(bg="white")
savings_menu.configure(bg="white")
paypal_menu.configure(bg="white")
# Call the update function initially to display selections
update_selection()

# Start the main event loop
root.mainloop()
