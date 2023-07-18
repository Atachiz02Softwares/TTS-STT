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

success = "Your transaction has been successfully done."
regards = "Thank you for patronage, we hope to see you again!"


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


def checkBalance():
    global pin, accountNumber  # Make pin and accountNumber global variables
    print("Checking balance, please hold on...")
    with open("Files/Accounts.csv", 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for i in reader:
            if int(i[1]) == pin and int(i[3]) == accountNumber:
                balance = i[2]
                speak(f"Your balance is: {balance}")
                print(f"Your balance is: {balance}")
                break
        else:
            speak("Balance not found for the user.")
            print("Balance not found for the user.")


intro()

wish()

user = ""

# Inputting and verifying pin and account number
speak("Please enter your 10-digit account number.")
flag1 = 1
flag2 = 0
while flag1:
    with open("Files/Accounts.csv", 'r') as file:
        t = 1
        reader = csv.reader(file, delimiter=',')
        l = []
        for i in reader:
            l.append(i)

        print("{*{Few example accounts loaded, please select one from below}*}")
        print(l)
        tries = 0

    while True:
        accountNumberInput = input("Enter your 10-digit account number: ").strip()

        if not accountNumberInput or not accountNumberInput.isdigit():
            speak("Please enter a valid 10-digit account number.")
            print("Please enter a valid 10-digit account number.")
            continue

        accountNumber = int(accountNumberInput)

        for i in l:
            if i[3] == str(accountNumber):  # Compare accountNumber as string from CSV
                tries = tries + 1
                break

        if tries == 0:
            print("Invalid account number, the account number does not exist.")
            speak("The account number is invalid.")
            attempts = attempts + 1
            if attempts == 3:
                print("You have exceeded the maximum number of trials, please try again later.")
                speak("You have exceeded the maximum number of trials, please try again later.")
                exit()
        else:
            user = i[0]
            print("Account number exists.")
            break

    if len(str(accountNumber)) == 10:
        flag1 = 0
        speak("Please say your 4-digit PIN number.")
        print("Please say your 4-digit PIN number.")
        while flag2 < 3 and flag1 == 0:
            try:
                pin = int(inputCommand().replace(" ", ""))  # Use voice input for PIN
            except Exception as error:
                print("Error: " + str(error))
                speak("Error")

            if len(str(pin)) == 4 and pin in [int(acc[1]) for acc in l]:  # Compare pin directly
                if [int(acc[1]) for acc in l].index(pin) == [int(acc[3]) for acc in l].index(accountNumber):
                    print("Accepted!")
                    speak("Accepted!")
                    flag1 = 0
                    break
                else:
                    print("Incorrect PIN. Please try again.")
                    speak("Incorrect PIN. Please try again.")
                    flag2 += 1

                if flag2 == 3:
                    speak("You have exceeded your maximum number of trials.")
                    exit()
    else:
        speak("Please enter a valid 10-digit account number.")
        print("Please enter a valid 10-digit account number.")

wish()
speak("Hello and Welcome!")
# speak(user)

print(
    "..........................................................CHOOSE FROM OPTIONS BELOW")
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

said = inputCommand()

# Code for withdrawing money.
if "withdraw" in said.lower() or "cash withdrawal" in said.lower():
    speak("You have chosen to withdraw cash.")
    # print("Enter denomination.")
    speak("Say or enter the amount you want to withdraw.")

    with open("Files/Accounts.csv", 'r') as file:
        t = 1
        reader = csv.reader(file, delimiter=',')
        l = []
        for i in reader:
            l.append(i)
        for i in l:
            i[1] = int(i[1])
            i[2] = float(i[2])

    trials = 0
    for i in l:
        if i[1] == pin:
            print(i[2])
            while True:
                amount = int(input())
                if amount > i[2]:
                    speak("The amount you wish to withdraw exceeds the amount you have in your account.")
                    speak("Please say or enter a valid amount.")
                    trials = trials + 1
                    if trials == 3:
                        speak("You have exceeded the number of trials.")
                        print("You have exceeded the number of trials.")
                        exit()
                elif amount < i[2]:
                    break

            i[2] -= amount
            print(i[2])
            t = 0
    print(l)

    file = open("Files/Accounts.csv", 'w', newline='')
    writer = csv.writer(file, delimiter=',')
    for i in range(len(l)):
        writer.writerow(l[i])
    file.close()
    speak(success + " Would you like to know your balance?")
    reply = inputCommand()

    if "Yes" in reply.lower() or "Yes please" in reply.lower() or "Yeah" in reply.lower() \
            or "Yes I would like to know my balance" in reply.lower():
        checkBalance()
    else:
        file.close()
        speak(regards)
        exit()

# Code for depositing cash.
elif "deposit" in said.lower() or "cash deposit" in said.lower():
    speak("You have chosen to deposit cash.")
    deposit = int(input("Enter the amount to deposit: "))

    with open("Files/Accounts.csv", 'r') as file:
        t = 1
        reader = csv.reader(file, delimiter=',')
        l = []
        for i in reader:
            l.append(i)
        for i in l:
            i[1] = int(i[1])
            i[2] = float(i[2])

        for i in l:
            if i[1] == pin:
                while True:
                    if deposit > 20000:
                        print("Please enter a valid amount to be deposited.")
                        speak("The amount you wish to deposit exceeds the limit, please enter a valid amount.")
                        deposit = int(input())
                    else:
                        break
                i[2] += deposit
                t = 0

    # Update the new appended balance in CSV file
    file = open("Files/Accounts.csv", 'w', newline='')
    writer = csv.writer(file, delimiter=',')
    for i in range(len(l)):
        writer.writerow(l[i])
    file.close()

    speak(success + " Would you like to know your balance?")
    check = inputCommand()
    if "No" in check.lower() or "No thank you" in check.lower():
        speak(regards)
        exit()
    else:
        checkBalance()
        speak(regards)
        exit()


# Code for checking balance.
elif "balance" in said.lower() or "balance inquiry" in said.lower():
    speak("You have selected to check your balance.")
    checkBalance()


# Code for changing PIN.
elif "change pin" in said.lower() or "change my pin" in said.lower():
    speak("You have chosen to change your PIN.")
    print("Please enter your old pin: ")
    tries = 0
    f = 1
    while f == 1:
        oldPin = int(input())
        if oldPin != pin:
            speak("Your pin does not match, please enter your old pin again.")
            print("Your pin does not match, please enter your old pin again:")
            tries = tries + 1
            if tries == 3:
                speak("You have exceeded the maximum number of trials.")
                exit()
        else:
            pinTrials = 0
            while f == 1:
                speak("Enter your new pin.")
                print("Enter your new pin:")
                newPin1 = int(input())
                if len(str(newPin1)) == 4:
                    speak("Please re-enter your new pin to confirm.")
                    print("Please re-enter your new pin to confirm:")
                    newPin2 = int(input())
                    if len(str(newPin2)) == 4:
                        if newPin1 == newPin2:
                            with open("Files/Accounts.csv", 'r') as file:
                                reader = csv.reader(file, delimiter=',')
                                l = []
                                for i in reader:
                                    l.append(i)
                                for i in l:
                                    i[1] = int(i[1])
                                    i[2] = float(i[2])
                                    if i[1] == oldPin and i[3] == accountNumber:
                                        i[1] = newPin1
                                        f = 0
                                        speak("Your new pin has been set successfully!")
                                        print("Your new pin has been set successfully!")
                                        speak(regards)
                            file = open("Files/Accounts.csv", 'w', newline='')
                            writer = csv.writer(file, delimiter=',')
                            for i in range(len(l)):
                                writer.writerow(l[i])
                            file.close()
                            exit()
                        else:
                            speak("The pin does not match, please try again.")
                            pinTrials = pinTrials + 1
                            if pinTrials == 3:
                                speak("You have exceeded the maximum number of trials.")
                                print("You have exceeded the maximum number of trials.")
                                exit()
                            print("The entered pin does not match, please try again.")

    speak("Your new pin has been set successfully!")
    print("Your new pin has been set successfully!")
    speak(regards)

    exit()

else:
    speak("Sorry! The command you entered does not exist, you will be taken back to the main menu.")
