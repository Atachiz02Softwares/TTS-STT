import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText

from main import write_accounts_data, read_accounts_data

welcome = ("\t\t\t************************************\n"
           "\t\t\t------------------------------------\n"
           "\t\t\tATM SYSTEM FOR THE VISUALLY IMPAIRED\n"
           "\t\t\t------------------------------------\n"
           "\t\t\t************************************\n"
           "\t\t\t   Powered by: Morpheus Softwares")


def write_current_accounts_data(file_name, account_data):
    with open(file_name, 'w', newline='') as file:
        fieldnames = ["pin", "accountNumber"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(account_data)


accounts_data = read_accounts_data("Files/Accounts.csv")
current_accounts_data = read_accounts_data("Files/CurrentlySignedInUser.csv")


# Function to verify login credentials
def login():
    account_number = account_number_entry.get()
    pin = pin_entry.get()
    account_data = [{"pin": pin, "accountNumber": account_number}]

    with open('Files/Accounts.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['accountNumber'] == account_number and row['pin'] == pin:
                write_current_accounts_data("Files/CurrentlySignedInUser.csv", account_data)
                messagebox.showinfo("Login Success", f"Welcome, {row['name']}!")
                window.destroy()  # Close the login window
                open_main_application()
                break
            else:
                messagebox.showerror("Login Failed", "Invalid account number or PIN")
                break


def withdraw():
    for r in current_accounts_data:
        for row in accounts_data:
            if int(r["pin"]) == int(row["pin"]) and int(r["accountNumber"]) == int(row["accountNumber"]):
                available_balance = float(row["balance"])
                while True:
                    try:
                        amount = int(simpledialog.askstring("Input", "Enter amount to withdraw:"))
                        if amount and amount <= available_balance:
                            row["balance"] = str(available_balance - amount)
                            write_accounts_data("Files/Accounts.csv", accounts_data)
                            messagebox.showinfo("Success",
                                                f"Withdrawal successful. Your new balance is {row['balance']}")
                            break
                        else:
                            messagebox.showerror("Error",
                                                 "The amount you want to withdraw exceeds your account balance.")
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid amount.")
                break
            else:
                messagebox.showerror("Error", "Account not found.")
                break


def deposit():
    for r in current_accounts_data:
        for row in accounts_data:
            if int(r["pin"]) == int(row["pin"]) and int(r["accountNumber"]) == int(row["accountNumber"]):
                while True:
                    amount = int(simpledialog.askstring("Input", "Enter amount to deposit:"))
                    try:
                        if amount <= 20000:
                            row["balance"] = str(float(row["balance"]) + amount)
                            write_accounts_data("Files/Accounts.csv", accounts_data)
                            messagebox.showinfo("Success", f"Deposit successful. Your new balance is {row['balance']}")
                            break
                        else:
                            messagebox.showerror("Error", "The amount you want to deposit exceeds the limit.")
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid amount.")
                break
            else:
                messagebox.showerror("Error", "Account not found.")
                break


def balance():
    for r in current_accounts_data:
        for row in accounts_data:
            if int(r["pin"]) == int(row["pin"]) and int(r["accountNumber"]) == int(row["accountNumber"]):
                available_balance = float(row["balance"])
                messagebox.showinfo("Info", f"Your balance is: {available_balance}")
                break
            else:
                messagebox.showerror("Error", "Balance not found for the cutomer.")
                break


def change_pin():
    tries = 0
    for r in current_accounts_data:
        for row in accounts_data:
            if int(r["pin"]) == int(row["pin"]) and int(r["accountNumber"]) == int(row["accountNumber"]):
                pin = int(row["pin"])
                while tries < 3:
                    oldPin = int(simpledialog.askstring("Input", "Please enter your old 4-digit PIN:"))
                    try:
                        oldPin = int(oldPin)
                        if oldPin == pin:
                            while True:
                                newPin1 = int(simpledialog.askstring("Input", "Enter your new 4-digit PIN."))
                                try:
                                    newPin1 = int(newPin1)
                                    if len(str(newPin1)) == 4:
                                        newPin2 = int(simpledialog.askstring("Input", "Please re-enter your new "
                                                                                      "4-digit PIN to confirm."))
                                        try:
                                            newPin2 = int(newPin2)
                                            if len(str(newPin2)) == 4 and newPin1 == newPin2:
                                                row["pin"] = str(newPin1)
                                                write_accounts_data("Files/Accounts.csv", accounts_data)
                                                messagebox.showinfo("Success",
                                                                    "Your new PIN has been set successfully!")
                                                break
                                            else:
                                                messagebox.showerror("Error",
                                                                     "The PINs you entered do not match. Please try "
                                                                     "again.")
                                                tries += 1
                                        except ValueError:
                                            messagebox.showerror("Error", "Please enter a valid 4-digit PIN.")
                                    else:
                                        messagebox.showerror("Error", "Please enter a valid 4-digit PIN.")
                                except ValueError:
                                    messagebox.showerror("Error", "Please enter a valid 4-digit PIN.")
                        else:
                            messagebox.showerror("Error", "Your old PIN does not match. Please try again.")
                            tries += 1
                            if tries == 3:
                                messagebox.showerror("Error", "You have exceeded the maximum number of trials.")
                                exit()
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid 4-digit PIN.")
                    break
            else:
                messagebox.showerror("Error", "Account not found.")
                break


# Function to open the main application
def open_main_application():
    win = tk.Tk()
    win.title("ATM")
    # win.geometry("600x500")

    # Display Screen
    displayScreen = ScrolledText(win, height=8)
    displayScreen.grid(row=2, column=1, padx=10, pady=10, columnspan=3)
    displayScreen.insert(tk.INSERT, welcome)

    cashWithdrawal = tk.Button(win, text="Cash Withdrawal", width=12, background="green", foreground="white",
                               command=withdraw)
    cashWithdrawal.grid(row=5, column=1, padx=5, pady=5)

    cashDeposit = tk.Button(win, text="Cash Deposit", width=12, background="brown", foreground="white", command=deposit)
    cashDeposit.grid(row=5, column=3, padx=5, pady=5)

    inputLabel = tk.Label(win, text="Input amount for withdrawal or deposit:", padx=5, pady=5)
    inputLabel.grid(row=5, column=2)

    value = tk.StringVar()
    amount = tk.Entry(win, textvariable=value, width=50)
    amount.grid(row=6, column=2)

    checkBalance = tk.Button(win, text="Check Balance", width=12, background="blue", foreground="white",
                             command=balance)
    checkBalance.grid(row=7, column=1, padx=5, pady=5)

    changePin = tk.Button(win, text="Change Pin", width=12, background="red", foreground="white", command=change_pin)
    changePin.grid(row=7, column=3, padx=5, pady=5)

    win.mainloop()


# Create the main window for login
window = tk.Tk()
window.title("Login Page")

# Create and place labels, entry fields, and buttons for login
account_number_label = tk.Label(window, text="Account Number:")
account_number_label.pack()

account_number_entry = tk.Entry(window)
account_number_entry.pack()

pin_label = tk.Label(window, text="PIN:")
pin_label.pack()

pin_entry = tk.Entry(window, show='*')  # Mask the PIN with asterisks
pin_entry.pack()

login_button = tk.Button(window, text="Login", background='green', foreground='white', command=login)
login_button.pack()

# Start the Tkinter main loop for the login window
window.mainloop()
