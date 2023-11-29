import csv
import datetime

import pyttsx4
import speech_recognition as sr

# Final global variables
attempts = 0

limit = 10000
minimum_limit = 100

success = "Your transaction has been done successfully..."
regards = "Thank you for patronage and for using this ATM system, we hope to see you again, goodbye!"


class Err(Exception):
    pass


engine = pyttsx4.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


def inputCommand():
    """
        Recognizes and returns user input through speech or text.

        Returns:
            str: The recognized input.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        said = r.recognize_google(audio, language="en-in")
        print(f"You said...: {said}\n")

    except Exception as e:
        print(e)
        print("Can you please say that again...")
        said = "Sorry, I did not understand that!"
    return said


# Greets user according to time of the day.
def wish():
    """
        Greets the user based on the time of the day.
    """
    hour = datetime.datetime.now().hour

    if 0 <= hour <= 12:
        speak("Good morning!")

    elif 12 <= hour < 18:
        speak("Good afternoon!")

    else:
        speak("Good evening!")


def speak(text):
    """
        Uses text-to-speech to speak the provided text.

        Args:
            text (str): The text to be spoken.
    """
    engine.say(text)
    engine.runAndWait()


def intro():
    """
        Displays the introduction to the ATM system.
    """
    print("\t\t\t\t************************************")
    print("\t\t\t\t------------------------------------")
    print("\t\t\t\tATM SYSTEM FOR THE VISUALLY IMPAIRED")
    print("\t\t\t\t------------------------------------")
    print("\t\t\t\t************************************")
    print("\t\t\t\t\tPowered by: Morpheus Softwares")


def read_accounts_data(file_name):
    """
        Reads and retrieves account data from a CSV file.

        Args:
            file_name (str): The name of the CSV file.

        Returns:
            list: A list of dictionaries containing account information.
    """
    with open(file_name, 'r', newline='') as file:
        reader = csv.DictReader(file)
        accounts_data = list(reader)
    return accounts_data


def write_accounts_data(file_name, accounts_data):
    """
        Writes account data to a CSV file.

        Args:
            file_name (str): The name of the CSV file to write to.
            accounts_data (list): A list of dictionaries containing account information.

        Returns:
            None
    """
    with open(file_name, 'w', newline='') as file:
        fieldnames = ["name", "pin", "balance", "accountNumber"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(accounts_data)


def checkBalance(accounts_data, pin, account_number):
    """
        Checks and displays the balance for a given account.

        Args:
            accounts_data (list): A list of dictionaries containing account information.
            pin (int): The PIN associated with the account.
            account_number (int): The account number for identification.

        Returns:
            None
    """
    print("Checking balance, please hold on...")
    for row in accounts_data:
        if int(row["pin"]) == pin and int(row["accountNumber"]) == account_number:
            balance = float(row["balance"])
            speak(f"Your balance is: {balance}")
            print(f"Your balance is: {balance}")
            break
        else:
            speak("Balance not found for the customer.")
            print("Balance not found for the customer.")
            break


def withdrawCash(accounts_data, pin, account_number):
    """
        Handles cash withdrawal from a specified account.

        Args:
            accounts_data (list): A list of dictionaries containing account information.
            pin (int): The PIN associated with the account.
            account_number (int): The account number for identification.

        Returns:
            None
    """
    speak("You have chosen to withdraw cash.")
    for row in accounts_data:
        if int(row["pin"]) == pin and int(row["accountNumber"]) == account_number:
            available_balance = float(row["balance"])
            while True:
                speak("Say or enter the amount you want to withdraw.")
                print("Say or enter the amount you want to withdraw:")
                amount = inputCommand().strip()
                try:
                    amount = int(amount)
                    if amount <= available_balance:
                        row["balance"] = str(available_balance - amount)
                        write_accounts_data("Files/Accounts.csv", accounts_data)
                        print(f"Withdrawal successful. Your new balance is {row['balance']}")
                        speak(f"Withdrawal successful. Your new balance is {row['balance']}")
                        break
                    else:
                        speak("The amount you want to withdraw exceeds your account balance.")
                        print("The amount you want to withdraw exceeds your account balance.")
                except ValueError:
                    speak("Please enter a valid amount.")
                    print("Please enter a valid amount.")
            break
        else:
            speak("Account not found.")
            print("Account not found.")
            break


def depositCash(accounts_data, pin, account_number):
    """
        Handles cash deposit to a specified account.

        Args:
            accounts_data (list): A list of dictionaries containing account information.
            pin (int): The PIN associated with the account.
            account_number (int): The account number for identification.

        Returns:
            None
    """
    speak("You have chosen to deposit cash.")
    for row in accounts_data:
        if int(row["pin"]) == pin and int(row["accountNumber"]) == account_number:
            while True:
                speak("Say or enter the amount you want to deposit.")
                print("Say or enter the amount you want to deposit:")
                amount = inputCommand().strip()
                try:
                    amount = int(amount)
                    if amount <= 20000:
                        row["balance"] = str(float(row["balance"]) + amount)
                        write_accounts_data("Files/Accounts.csv", accounts_data)
                        print(f"Deposit successful. Your new balance is {row['balance']}")
                        speak(f"Deposit successful. Your new balance is {row['balance']}")
                        break
                    else:
                        speak("The amount you want to deposit exceeds the limit.")
                        print("The amount you want to deposit exceeds the limit.")
                except ValueError:
                    speak("Please enter a valid amount.")
                    print("Please enter a valid amount.")
            break
        else:
            speak("Account not found.")
            print("Account not found.")
            break


def changePin(accounts_data, pin, account_number):
    """
       Allows the user to change their PIN.

       Args:
           accounts_data (list): A list of dictionaries containing account information.
           pin (int): The PIN associated with the account.
           account_number (int): The account number for identification.

       Returns:
           None
    """
    speak("You have chosen to change your PIN.")
    tries = 0
    for row in accounts_data:
        if int(row["pin"]) == pin and int(row["accountNumber"]) == account_number:
            while tries < 3:
                speak("Please enter your old 4-digit PIN.")
                print("Please enter your old 4-digit PIN:")
                oldPin = inputCommand().strip()
                try:
                    oldPin = int(oldPin)
                    if oldPin == pin:
                        while True:
                            speak("Enter your new 4-digit PIN.")
                            print("Enter your new 4-digit PIN:")
                            newPin1 = inputCommand()
                            try:
                                newPin1 = int(newPin1)
                                if len(str(newPin1)) == 4:
                                    speak("Please re-enter your new 4-digit PIN to confirm.")
                                    print("Please re-enter your new 4-digit PIN to confirm:")
                                    newPin2 = inputCommand()
                                    try:
                                        newPin2 = int(newPin2)
                                        if len(str(newPin2)) == 4 and newPin1 == newPin2:
                                            row["pin"] = str(newPin1)
                                            write_accounts_data("Files/Accounts.csv", accounts_data)
                                            print("Your new PIN has been set successfully!")
                                            speak("Your new PIN has been set successfully!")
                                            break
                                        else:
                                            speak("The PINs you entered do not match. Please try again.")
                                            print("The PINs you entered do not match. Please try again.")
                                            tries += 1
                                    except ValueError:
                                        speak("Please enter a valid 4-digit PIN.")
                                        print("Please enter a valid 4-digit PIN.")
                                else:
                                    speak("Please enter a valid 4-digit PIN.")
                                    print("Please enter a valid 4-digit PIN.")
                            except ValueError:
                                speak("Please enter a valid 4-digit PIN.")
                                print("Please enter a valid 4-digit PIN.")
                    else:
                        speak("Your old PIN does not match. Please try again.")
                        print("Your old PIN does not match. Please try again.")
                        tries += 1
                        if tries == 3:
                            speak("You have exceeded the maximum number of trials.")
                            print("You have exceeded the maximum number of trials.")
                            exit()
                except ValueError:
                    speak("Please enter a valid 4-digit PIN.")
                    print("Please enter a valid 4-digit PIN.")
                break
        else:
            speak("Account not found.")
            print("Account not found.")
            break


def main():
    """
        Entry point of the ATM system program.

        Manages user interaction and navigation within the ATM system.

        Returns:
            None
    """
    intro()
    wish()

    # Inputting and verifying pin and account number
    while True:
        accounts_data = read_accounts_data("Files/Accounts.csv")

        print("Few example accounts loaded, please select one from below:")
        print(accounts_data)
        speak("Say your 10-digit account number.")

        # Trim spaces or unwanted characters and remove white spaces
        accountNumberInput = inputCommand().strip().replace(" ", "")

        if not accountNumberInput or not accountNumberInput.isdigit():
            speak("Please say a valid 10-digit account number.")
            print("Please say a valid 10-digit account number.")
            continue

        account_number = int(accountNumberInput)
        attempts = 0

        user = None
        for row in accounts_data:
            if int(row["accountNumber"]) == account_number:
                user = row["name"]
                pin = int(row["pin"])
                break

        if user is None:
            print("Invalid account number, the account number does not exist.")
            speak("The account number is invalid.")
            attempts += 1
            if attempts == 3:
                print("You have exceeded the maximum number of trials, please try again later.")
                speak("You have exceeded the maximum number of trials, please try again later.")
                exit()
        else:
            print("Account number exists.")
            break

    if len(str(account_number)) == 10:
        speak("Please enter your 4-digit PIN number.")
        print("Please enter your 4-digit PIN number.")
        while True:
            try:
                pin_input = inputCommand().strip().replace(" ", "")
                pin = int(pin_input)
                if len(str(pin)) == 4:
                    if pin == pin:
                        print("Accepted!")
                        speak("Accepted!")
                        break
                    else:
                        print("Incorrect PIN. Please try again.")
                        speak("Incorrect PIN. Please try again.")
                else:
                    speak("Please enter a valid 4-digit PIN.")
                    print("Please enter a valid 4-digit PIN.")
            except ValueError:
                speak("Please enter a valid 4-digit PIN.")
                print("Please enter a valid 4-digit PIN.")

    else:
        speak("Please enter a valid 10-digit account number.")
        print("Please enter a valid 10-digit account number.")
        exit()

    speak("Hello and Welcome!")

    while True:
        print("..........................................................CHOOSE FROM OPTIONS BELOW")
        print("")
        speak("Please select from the options below.")
        print(
            "\t\t\t\t\t(1) CASH WITHDRAWAL                                (2) CASH DEPOSIT"
            "              ")
        speak("1. Cash Withdrawal. 2. Cash Deposit")
        print(
            "\t\t\t\t\t(3) BALANCE INQUIRY                                (4) CHANGE PIN"
            "              ")
        speak("3. Balance Inquiry. 4. Change Pin")
        print(
            ".........................................................................................................."
            ".............................")

        option = inputCommand().strip()

        if "withdraw" in option.lower() or "cash withdrawal" in option.lower():
            withdrawCash(accounts_data, pin, account_number)
        elif "deposit" in option.lower() or "cash deposit" in option.lower():
            depositCash(accounts_data, pin, account_number)
        elif "balance" in option.lower() or "balance inquiry" in option.lower():
            checkBalance(accounts_data, pin, account_number)
        elif "change pin" in option.lower() or "change my pin" in option.lower():
            changePin(accounts_data, pin, account_number)
        else:
            speak("Sorry! The command you entered does not exist, please try again.")
            print("Sorry! The command you entered does not exist, please try again.")

        # Ask if the user wants to continue or exit
        speak("Would you like to continue or exit?")
        print("Would you like to continue or exit? (Say 'Continue' or 'Exit')")
        continue_exit = inputCommand().lower()
        if "continue" in continue_exit:
            main()
        elif "exit" in continue_exit:
            speak(regards)
            exit()


if __name__ == "__main__":
    main()
