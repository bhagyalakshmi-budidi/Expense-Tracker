import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"

# Initialize file
def init_file():
    try:
        with open(FILE_NAME, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Amount", "Category", "Description", "Date"])
    except FileExistsError:
        pass


# Add expense
def add_expense():
    amount = amount_entry.get()
    category = category_var.get()
    desc = desc_entry.get()

    if amount == "":
        messagebox.showerror("Error", "Enter amount")
        return

    try:
        float(amount)
    except:
        messagebox.showerror("Error", "Amount must be number")
        return

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([amount, category, desc, date])

    messagebox.showinfo("Success", "Expense Added!")

    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)

    load_data()


# Load data into table
def load_data():
    for row in tree.get_children():
        tree.delete(row)

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                tree.insert("", tk.END, values=row)
    except:
        pass


# Delete last expense
def delete_last():
    try:
        with open(FILE_NAME, "r") as file:
            rows = list(csv.reader(file))

        if len(rows) <= 1:
            messagebox.showerror("Error", "No data to delete")
            return

        rows.pop()

        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        messagebox.showinfo("Deleted", "Last expense removed")
        load_data()

    except:
        messagebox.showerror("Error", "Something went wrong")


# Total expense
def total_expense():
    total = 0
    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            total += float(row["Amount"])

    messagebox.showinfo("Total", f"Total Expense: {total}")


# Monthly report
def monthly_report():
    month = month_entry.get()
    total = 0

    if month == "":
        messagebox.showerror("Error", "Enter month YYYY-MM")
        return

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Date"].startswith(month):
                total += float(row["Amount"])

    messagebox.showinfo("Monthly", f"{month} Total: {total}")


# Chart
def show_chart():
    data = {}

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cat = row["Category"]
            amt = float(row["Amount"])
            data[cat] = data.get(cat, 0) + amt

    if not data:
        messagebox.showerror("Error", "No data")
        return

    plt.pie(data.values(), labels=data.keys(), autopct="%1.1f%%")
    plt.title("Expense Distribution")
    plt.show()


# GUI
root = tk.Tk()
root.title("Expense Tracker Pro")
root.geometry("600x500")

init_file()

# Inputs
tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Category").pack()
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(root, textvariable=category_var)
category_dropdown['values'] = ("Food", "Travel", "Shopping", "Other")
category_dropdown.current(0)
category_dropdown.pack()

tk.Label(root, text="Description").pack()
desc_entry = tk.Entry(root)
desc_entry.pack()

tk.Label(root, text="Month (YYYY-MM)").pack()
month_entry = tk.Entry(root)
month_entry.pack()

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).pack(pady=5)
tk.Button(root, text="Delete Last", command=delete_last).pack(pady=5)
tk.Button(root, text="Total Expense", command=total_expense).pack(pady=5)
tk.Button(root, text="Monthly Report", command=monthly_report).pack(pady=5)
tk.Button(root, text="Show Chart 📊", command=show_chart).pack(pady=5)

# Table
columns = ("Amount", "Category", "Description", "Date")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True)

load_data()

root.mainloop()