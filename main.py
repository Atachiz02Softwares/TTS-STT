import pyttsx4
import random
from gtts import gTTS
import speech_recognition as sr
import os
import csv

import datetime

# Final global variables
attempts = 0

limit = 10000
minimumLimit = 100

success = "Your transaction has been done successfully..."
regards = "Thank you for patronage and for using this ATM system, we hope to see you again, goodbye!"


class Err(Exception):
    pass


engine = pyttsx4.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


def inputCommand():
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
    hour = datetime.datetime.now().hour

    if 0 <= hour <= 12:
        speak("Good morning!")

    elif 12 <= hour < 18:
        speak("Good afternoon!")

    else:
        speak("Good evening!")


def speak(text):
    engine.say(text)
    engine.runAndWait()


def intro():
    print("\t\t\t\t************************************")
    print("\t\t\t\t------------------------------------")
    print("\t\t\t\tATM SYSTEM FOR THE VISUALLY IMPAIRED")
    print("\t\t\t\t------------------------------------")
    print("\t\t\t\t************************************")
    print("\t\t\t\t\tPowered by: Morpheus Softwares")


def read_accounts_data():
    with open("Files/Accounts.csv", 'r', newline='') as file:
        reader = csv.DictReader(file)
        accounts_data = list(reader)
    return accounts_data


def write_accounts_data(accounts_data):
    with open("Files/Accounts.csv", 'w', newline='') as file:
        fieldnames = ["name", "pin", "balance", "accountNumber"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(accounts_data)


def checkBalance(accounts_data, pin, accountNumber):
    print("Checking balance, please hold on...")
    for row in accounts_data:
        if int(row["pin"]) == pin and int(row["accountNumber"]) == accountNumber:
            balance = float(row["balance"])
            speak(f"Your balance is: {balance}")
            print(f"Your balance is: {balance}")
            break
    else:
        speak("Balance not found for the user.")
        print("Balance not found for the user.")


def withdrawCash(accounts_data, pin, accountNumber):
    speak("You have chosen to withdraw cash.")
    for row in accounts_data:
        if int(row["pin"]) == pin and int(row["accountNumber"]) == accountNumber:
            available_balance = float(row["balance"])
            while True:
                speak("Say or enter the amount you want to withdraw.")
                print("Say or enter the amount you want to withdraw:")
                amount = inputCommand()
                try:
                    amount = int(amount)
                    if amount <= available_balance:
                        row["balance"] = str(available_balance - amount)
                        write_accounts_data(accounts_data)
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


def depositCash(accounts_data, pin, accountNumber):
    speak("You have chosen to deposit cash.")
    for row in accounts_data:
        if int(row["pin"]) == pin and int(row["accountNumber"]) == accountNumber:
            while True:
                speak("Say or enter the amount you want to deposit.")
                print("Say or enter the amount you want to deposit:")
                amount = inputCommand()
                try:
                    amount = int(amount)
                    if amount <= 20000:
                        row["balance"] = str(float(row["balance"]) + amount)
                        write_accounts_data(accounts_data)
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


def changePin(accounts_data, pin, accountNumber):
    speak("You have chosen to change your PIN.")
    tries = 0
    for row in accounts_data:
        if int(row["pin"]) == pin and int(row["accountNumber"]) == accountNumber:
            while tries < 3:
                speak("Please enter your old 4-digit PIN.")
                print("Please enter your old 4-digit PIN:")
                oldPin = inputCommand()
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
                                            write_accounts_data(accounts_data)
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


def main():
    intro()
    wish()

    # Inputting and verifying pin and account number
    while True:
        accounts_data = read_accounts_data()

        print("Few example accounts loaded, please select one from below:")
        print(accounts_data)
        speak("Enter your 10-digit account number.")
        accountNumberInput = input("Enter your 10-digit account number: ").strip()

        if not accountNumberInput or not accountNumberInput.isdigit():
            speak("Please enter a valid 10-digit account number.")
            print("Please enter a valid 10-digit account number.")
            continue

        accountNumber = int(accountNumberInput)
        attempts = 0

        user = None
        for row in accounts_data:
            if int(row["accountNumber"]) == accountNumber:
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

    if len(str(accountNumber)) == 10:
        speak("Please enter your 4-digit PIN number.")
        print("Please enter your 4-digit PIN number.")
        while True:
            try:
                pin_input = inputCommand()
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
            ".................................................................................................................."
            ".....................")

        option = inputCommand()

        if "withdraw" in option.lower() or "cash withdrawal" in option.lower():
            withdrawCash(accounts_data, pin, accountNumber)
        elif "deposit" in option.lower() or "cash deposit" in option.lower():
            depositCash(accounts_data, pin, accountNumber)
        elif "balance" in option.lower() or "balance inquiry" in option.lower():
            checkBalance(accounts_data, pin, accountNumber)
        elif "change pin" in option.lower() or "change my pin" in option.lower():
            changePin(accounts_data, pin, accountNumber)
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
