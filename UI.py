import tkinter as tk


def deposit():
    # Add code to handle deposit functionality here
    print("Deposit")


def withdraw():
    # Add code to handle withdrawal functionality here
    print("Withdraw")


def balance():
    # Add code to handle balance checking functionality here
    print("Balance")


def transfer():
    # Add code to handle transfer functionality here
    print("Transfer")


def exit_app():
    # Add code to handle exit functionality here
    print("Exit")


# Create the main window
window = tk.Tk()
window.title("ATM")

# Create a frame for buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=20)

# Create the buttons with different colors
deposit_btn = tk.Button(button_frame, text="Deposit", width=15, command=deposit, bg="green", fg="white")
deposit_btn.pack(side=tk.LEFT, padx=10)

withdraw_btn = tk.Button(button_frame, text="Withdraw", width=15, command=withdraw, bg="blue", fg="white")
withdraw_btn.pack(side=tk.LEFT, padx=10)

balance_btn = tk.Button(button_frame, text="Balance", width=15, command=balance, bg="orange", fg="white")
balance_btn.pack(side=tk.LEFT, padx=10)

transfer_btn = tk.Button(button_frame, text="Transfer", width=15, command=transfer, bg="purple", fg="white")
transfer_btn.pack(side=tk.LEFT, padx=10)

exit_btn = tk.Button(window, text="Exit", width=15, command=exit_app, bg="red", fg="white")
exit_btn.pack(pady=10)

# Start the main event loop
window.mainloop()
