import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from connect import *
from datetime import datetime


# Creating the root window
root = tk.Tk()
root.title("Finance Tracking Application")
root.configure(bg='pink')
root.geometry("800x800")
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Function to update header and footer based on frame name
def update_header_footer(frame_name):
    header_label.config(text=header_texts[frame_name])
    footer_button.config(text=footer_texts[frame_name], command=footer_commands[frame_name])

# Function to show a certain frame when a button is pressed
def show_frame(frame, frame_name):
    update_header_footer(frame_name)
    frame.tkraise()


def gui_add_expense(): # Function to take user inputs and parse it into insert_expense which stores in MySQL
    validation = True # To check if all inputs are given, starts off as True
    errorOutput = tk.StringVar() # To give the corresponding output based on the error
    outputLabel = tk.Label(add_menu, textvariable=errorOutput, width=30)
    outputLabel.grid(row=6, column=1)

    date_input = addDateInput.get_date()
    category_input = addCategoryInput.get("1.0", tk.END).strip()
    description_input = addDescriptionInput.get("1.0", tk.END).strip()
    amount_input = addAmountInput.get("1.0", tk.END).strip()    
    
    try:
        amount_input = float(amount_input) # Try to convert to float, if it fails then return error
    except ValueError:
        errorOutput.set("Please enter a number")
        validation = False
    if not (date_input and category_input and description_input and amount_input):
        errorOutput.set("Please fill in all blanks")
        validation = False
    if validation:
        insert_expense(date_input, category_input, description_input, amount_input)
        add_menu_treeview()
        errorOutput.set("Expense saved successfully")
    

def gui_delete_expense(): # Function to take user inputs and parse it into delete_expense which deletes an expense stored in MySQL
    trans_id_input = deleteTransIDInput.get("1.0", tk.END).strip()
    errorOutput = tk.StringVar()
    outputLabel = tk.Label(delete_menu, textvariable=errorOutput, width=30)
    outputLabel.grid(row=3, column=1)
    validation = True # To check if all inputs are given, starts off as True
    if not trans_id_input:
        errorOutput.set("Please enter a transaction ID")
        validation = False
    if validation:
        delete_expense(trans_id_input)
        delete_menu_treeview()
        errorOutput.set("Expense deleted successfully")

def gui_edit_expense(): # To edit an expense in MySQL
    validation = True
    errorOutput = tk.StringVar() 
    outputLabel = tk.Label(edit_menu, textvariable=errorOutput, width=30)
    outputLabel.grid(row=8, column=1)
    trans_id_input = editTransIDInput.get("1.0", tk.END).strip()
    date_input = editDateInput.get_date().strftime('%Y-%m-%d')
    category_input = editCategoryInput.get("1.0", tk.END).strip()
    description_input = editDescriptionInput.get("1.0", tk.END).strip()
    amount_input = editAmountInput.get("1.0", tk.END).strip()
    if not (trans_id_input and date_input and category_input and description_input and amount_input):
        validation = False
        errorOutput.set("Please fill in all blanks")
    if validation:
        edit_expenses(trans_id_input, date_input, category_input, description_input, amount_input)
        edit_menu_treeview()
        errorOutput.set("Expense updated succesfully")
    
def gui_get_expense_details(): # To get info from MySQL table based on transaction ID 
    validation = True
    errorOutput = tk.StringVar() 
    outputLabel = tk.Label(edit_menu, textvariable=errorOutput, width=40)
    outputLabel.grid(row=8, column=1)
    trans_id_input = editTransIDInput.get("1.0", tk.END).strip()
    if not trans_id_input:
        errorOutput.set("Please enter a transaction ID")
        validation = False
    if validation: # If trans_id is entered, run the functon to get expense info
        expense_info = get_expense_info(trans_id_input)
        if expense_info is None:
            errorOutput.set("Info not found. Please enter a valid transaction ID")
            validation = False
    transDetails, date_str_from_mysql, categoryDetails, descriptionDetails, amountDetails = expense_info # Only date is returned as a str. Needs to be converted to datetime obj

    try:
        date_obj = datetime.strptime(date_str_from_mysql, '%Y-%m-%d') # Converts the str to datetime object
    except ValueError as error:
        print(error)
        return 
    editDateInput.set_date(date_obj)
    editCategoryInput.delete("1.0", tk.END)
    editCategoryInput.insert(tk.END, categoryDetails)
    editDescriptionInput.delete("1.0", tk.END)
    editDescriptionInput.insert(tk.END, descriptionDetails)
    editAmountInput.delete("1.0", tk.END)
    editAmountInput.insert(tk.END, amountDetails)
    
        
def add_menu_treeview(): # Function to display the expenses correctly on the tree view in the add menu
    for i in addMenuTreeView.get_children():
        addMenuTreeView.delete(i) #Clears the existing rows and updates it with a new list when an expense is added  
    expenses_list, column_names = view_expenses() # Gets the expense list from the data table in MySQL
    addMenuTreeView["columns"] = column_names
    addMenuTreeView["show"] = "headings"  # Hide the default column
    for col in column_names:
        addMenuTreeView.column(col, width=100)
        addMenuTreeView.heading(col, text=col)
    for expense in expenses_list:
        addMenuTreeView.insert("", "end", values=expense)

def delete_menu_treeview(): # Function to display the expenses correctly on the tree view in the delete menu
    for i in deleteMenuTreeView.get_children():
        deleteMenuTreeView.delete(i)
    expenses_list, column_names = view_expenses()
    deleteMenuTreeView["columns"] = column_names
    deleteMenuTreeView["show"] = "headings"  # Hide the default column
    for col in column_names:
        deleteMenuTreeView.heading(col, text=col)
        deleteMenuTreeView.column(col, width=100)
    for expense in expenses_list:
        deleteMenuTreeView.insert("", "end", values=expense)

def edit_menu_treeview(): # Function to display the expenses correctly on the tree view in the delete menu
    for i in editMenuTreeView.get_children():
        editMenuTreeView.delete(i)
    expenses_list, column_names = view_expenses()
    editMenuTreeView["columns"] = column_names
    editMenuTreeView["show"] = "headings"  # Hide the default column
    for col in column_names:
        editMenuTreeView.heading(col, text=col)
        editMenuTreeView.column(col, width=100)
    for expense in expenses_list:
        editMenuTreeView.insert("", "end", values=expense)

# Dictionaries to store header texts, footer texts, and footer commands for each frame
header_texts = {
    "main_menu": "Welcome to the Finance App. Please select an option.",
    "add_menu": "Please key in the expense details.",
    "edit_menu": "Please choose an expense to edit",
    "delete_menu": "Please key in an expense transaction ID to delete.",
    "view_menu": "View your expenses."
}

footer_texts = {
    "main_menu": "Quit",
    "add_menu": "Back",
    "edit_menu": "Back",
    "delete_menu": "Back",
    "view_menu": "Back"
}

footer_commands = {
    "main_menu": root.destroy,
    "add_menu": lambda: show_frame(main_menu, "main_menu"),
    "edit_menu": lambda: show_frame(main_menu, "main_menu"),
    "delete_menu": lambda: show_frame(main_menu, "main_menu"),
    "view_menu": lambda: show_frame(main_menu, "main_menu")
}

# Creating the frames
main_menu = tk.Frame(root, background="bisque")
main_menu.grid(row=1, column=0, sticky="nsew")
add_menu = tk.Frame(root, background ="bisque")
add_menu.grid(row=1, column=0, sticky="nsew")
edit_menu = tk.Frame(root, background ="bisque")
edit_menu.grid(row=1, column=0, sticky="nsew")
delete_menu = tk.Frame(root, background = 'bisque')
delete_menu.grid(row=1, column=0, sticky="nsew")
view_menu = tk.Frame(root)
view_menu.grid(row=1, column=0, sticky="nsew")

# Creating the labels
header_label = tk.Label(root, text='Welcome to the Finance App. Please select an option.', bg='pink')
header_label.grid(row=0, column=0)

footer_button = tk.Button(root, text='Quit', width=10, height=2, command=root.destroy)
footer_button.grid(row=2, column=0)

# Setting up the main menu GUI alongside the buttons
tk.Label(main_menu, text='Add an Expense', bg='bisque').grid(row=0, column=0, sticky='w')
tk.Label(main_menu, text='Delete an Expense', bg='bisque').grid(row=1, column=0, sticky='w')
tk.Label(main_menu, text='Edit an Expense', bg='bisque').grid(row=2, column=0, sticky='w')
tk.Label(main_menu, text='View Expenses', bg='bisque').grid(row=3, column=0, sticky='w')

tk.Button(main_menu, text='Add', width=10, height=2, command=lambda: show_frame(add_menu, "add_menu")).grid(row=0, column=1, padx=5, pady=5, sticky='w')
tk.Button(main_menu, text='Delete', width=10, height=2, command=lambda: show_frame(delete_menu, "delete_menu")).grid(row=1, column=1, padx=5, pady=5, sticky='w')
tk.Button(main_menu, text='Edit', width=10, height=2, command=lambda: show_frame(edit_menu, "edit_menu")).grid(row=2, column=1, padx=5, pady=5, sticky='w')
tk.Button(main_menu, text='View', width=10, height=2, command=lambda: show_frame(view_menu, "view_menu")).grid(row=3, column=1, padx=5, pady=5, sticky='w')


# Setting up the add expense menu GUI
tk.Label(add_menu, text='Date', bg='bisque').grid(row=0, column=0, padx=5, pady=5, sticky='w')

# Input must be separated otherwise it would return None if .grid is appended to the end
addDateInput = DateEntry(add_menu, width=20, bg='white', year=2024, month=6, day=17)
addDateInput.grid(row=0, column=1, padx=5, pady=5, sticky='w')
tk.Label(add_menu, text='Category', bg='bisque').grid(row=1, column=0, padx=5, pady=5, sticky='w')
addCategoryInput = tk.Text(add_menu, height=1, width=20,bg='white')
addCategoryInput.grid(row=1, column=1, padx=5, pady=5, sticky='w')
tk.Label(add_menu, text='Description', bg='bisque').grid(row=2, column=0, padx=5, pady=5, sticky='w')
addDescriptionInput = tk.Text(add_menu, height=1, width=20,bg='white')
addDescriptionInput.grid(row=2, column=1, padx=5, pady=5, sticky='w')
tk.Label(add_menu, text='Amount', bg='bisque').grid(row=3, column=0, padx=5, pady=5, sticky='w')
addAmountInput = tk.Text(add_menu, height=1, width=20,bg='white')
addAmountInput.grid(row=3, column=1, padx=5, pady=5, sticky='w')
saveAddMenuButton = tk.Button(add_menu, text='Add Expense', command=gui_add_expense).grid(row=4, column=1, padx=5, pady=5, sticky='w')

addMenuTreeView = ttk.Treeview(add_menu)
addMenuTreeView.grid(row=5, column=1, padx=5, pady=5, sticky='w')
add_menu_treeview()

# Setting up the delete expense menu GUI
# Here users can view the list of expenses and delete whichever they want to, based on trans_id
tk.Label(delete_menu, text='Transaction ID', bg='bisque').grid(row=0, column=0, padx=5, pady=5, sticky='w')
deleteTransIDInput = tk.Text(delete_menu, height=1, width=20,bg='white')
deleteTransIDInput.grid(row=0, column=1, padx=5, pady=5, sticky='w')
saveDeleteMenuButton = tk.Button(delete_menu, text='Delete Expense', command=gui_delete_expense).grid(row=1, column=1, padx=5, pady=5, sticky='w')
deleteMenuTreeView = ttk.Treeview(delete_menu)
deleteMenuTreeView.grid(row=2, column=1, padx=5, pady=5, sticky='w')
delete_menu_treeview()

# Setting up the update expense menu GUI
# Users will be able to update expenses here

editMenuTreeView = ttk.Treeview(edit_menu)
editMenuTreeView.grid(row=7, column=1, padx=5, pady=5, sticky='w')

tk.Label(edit_menu, text='Transaction ID', bg='bisque').grid(row=0, column=0, padx=5, pady=5, sticky='w')
editTransIDInput = tk.Text(edit_menu, height=1, width=20,bg='white')
editTransIDInput.grid(row=0, column=1, padx=5, pady=5, sticky='w')
tk.Label(edit_menu, text='Date', bg='bisque').grid(row=2, column=0, padx=5, pady=5, sticky='w')
editDateInput = DateEntry(edit_menu, width=20, bg='white', year=2024, month=6, day=17)
editDateInput.grid(row=2, column=1, padx=5, pady=5, sticky='w')
tk.Label(edit_menu, text='Category', bg='bisque').grid(row=3, column=0, padx=5, pady=5, sticky='w')
editCategoryInput = tk.Text(edit_menu, height=1, width=20,bg='white')
editCategoryInput.grid(row=3, column=1, padx=5, pady=5, sticky='w')
tk.Label(edit_menu, text='Description', bg='bisque').grid(row=4, column=0, padx=5, pady=5, sticky='w')
editDescriptionInput = tk.Text(edit_menu, height=1, width=20,bg='white')
editDescriptionInput.grid(row=4, column=1, padx=5, pady=5, sticky='w')
tk.Label(edit_menu, text='Amount', bg='bisque').grid(row=5, column=0, padx=5, pady=5, sticky='w')
editAmountInput = tk.Text(edit_menu, height=1, width=20,bg='white')
editAmountInput.grid(row=5, column=1, padx=5, pady=5, sticky='w')
editMenuButton = tk.Button(edit_menu, text='Edit Expense', command=gui_edit_expense).grid(row=6, column=1, padx=5, pady=5, sticky='w')
editMenuGetInfoButton = tk.Button(edit_menu, text='Get Expense Info', command=gui_get_expense_details).grid(row=1, column=1, padx=5, pady=5, sticky='w')
edit_menu_treeview()

# Start with the main menu frame
show_frame(main_menu, "main_menu")

root.mainloop()
