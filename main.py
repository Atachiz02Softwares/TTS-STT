import pyttsx3
import random
from gtts import gTTS
import speech_recognition as sr
import os
import csv
import getpass_asterisk
import datetime

# Final global variables
attempts = 0

limit = 10000
minimumLimit = 100

success = "Your transaction has been successfully done."
regards = "Thank you for patronage, we hope to see you again!"


class Err(Exception):
    pass


engine = pyttsx3.init()
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
        print(f"You said...: {said}\n", )


    except Exception as e:
        print(e)
        print("Can you please say that again...")
        said = "Sorry, I did not understand that!"
    return said


# Greets user according to time of the day.

def wish():
    hour = datetime.datetime.now().hour

    if hour >= 0 and hour <= 12:
        speak("Good morning!")

    elif hour >= 12 and hour < 18:
        speak("Good afternoon!")

    else:
        speak("Good evening!")


def speak(text):
    engine.say(text)
    engine.runAndWait()


def intro():
    print("")
    print("")
    print("\t\t\t\t@ ************************************* @")
    print("\t\t\t\t# ------------------------------------- #")
    print("\t\t\t\t  ATM SYSTEM FOR THE VISUALLY IMPAIRED   ")
    print("\t\t\t\t# ------------------------------------- #")
    print("\t\t\t\t@ ************************************* @")
    print("")
    print("")
    print("\t\t\t\tBrought To You By:")
    print("\t\t\t\tMorpheus Softwares")
    input()


intro()

wish()

"""
eng= "To select English as a language, please press one."
obj = gTTS(text= eng , slow = False , lang ='en')
obj.save('eng.mp3')
speak(eng)
"""

user = ""

# Inputting and verifying pin and account number

speak("Please, enter your 10-digits account number.")
flag1 = 1
flag2 = 0
while flag1:
    with open("Files/Accounts.csv", 'r') as file:
        t = 1
        reader = csv.reader(file, delimiter=',')
        l = []
        l1 = []
        l2 = []
        for i in reader:
            l.append(i)
        for i in l:
            i[1] = int(i[1])
            i[2] = float(i[2])
            l1.append(i[1])
            l2.append(int(i[3]))

        print("{*{Few example accounts loaded, please select one from below}*}")
        print(l)
        tries = 0

    while True:
        accountNumber = input("Enter your 10-digits account number:")
        for i in l:
            if i[3] == accountNumber:
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

    if accountNumber.isdigit() and len(accountNumber) == 10:  # If accountNumber is equal to 10, then:
        flag1 = 0
        speak("Please enter your 4-digits pin number.")
        print("Please enter your 4-digits pin number.")
        while flag2 < 3:
            try:
                pin = getpass_asterisk.getpass()

            except Exception as error:
                print("Error: " + error)
                speak("Error")

            # If pin is equal to 4 and is in the list of pins...
            if pin.isdigit() and len(pin) == 4 and int(pin) in l1:
                # If the pin is the corresponding pin of the inputted account number, then:
                if l1.index(int(pin)) == l2.index(int(accountNumber)):
                    # Check with pin in file, and replace the pin with '*'
                    flag1 = 0
                    flag2 = 3
                    print("Accepted!")
                    speak("Accepted!")
                else:
                    print("Pin does not match.")
                    speak("Pin does not match.")
                # continue to regular code
            else:
                print("Please, end  your correct pin.")
                speak("Please, end your correct pin.")
                flag2 += 1
                if flag2 == 3:
                    speak("You have exceeded your maximum number of trials.")
                    exit()

    else:
        speak("Please, enter a valid 10-digits account number.")
        print("Please, enter a valid 10-digits account number.")

wish()
speak("Hello and Welcome!")
speak(user)

print(
    "..........................................................CHOOSE FROM OPTIONS "
    "BELOW....................................................")
print("")

speak("Please, select from the options below.")
print(
    "\t\t\t\t\t(1)CASH WITHDRAWAL                                (2)CASH DEPOSIT                                      "
    "              ")
speak("1. Cash Withdrawal. 2. Cash Deposit")
print(
    "\t\t\t\t\t(3)BALANCE INQUIRY                                (4)CHANGE PIN                                        "
    "              ")
speak("3. Balance Inquiry. 4. Change Pin")
print(
    ".................................................................................................................."
    ".....................")

said = inputCommand()

# Code for withdrawing money.

if "Cash withdrawal" in said.lower() or "withdraw some cash" in said.lower() or "withdraw" in said.lower() \
        or "Withdraw cash" in said.lower():
    speak("You have chosen to withdraw cash.")
    print("Enter denomination.")
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
        if i[1] == int(pin):
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
        with open("Files/Accounts.csv", 'r') as file:
            reader = csv.reader(file, delimiter=',')
            a = []
            for i in reader:
                a.append(i)

            for i in a:
                if i[1] == int(pin):
                    speak(f"Your balance is: {i[2]}")
                    print(f"Your balance is: {i[2]}")

    else:
        file.close()
        speak(regards)
        exit()

# Code for depositing cash.

elif "Cash deposit" in said.lower() or "Deposit some cash" in said.lower() or "Deposit cash" in said.lower() \
        or "Deposit" in said.lower():
    speak("You have chosen to deposit cash, enter the amount to be deposited.")
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
            if i[1] == int(pin):
                while True:
                    if deposit > 20000:
                        print("Please, enter a valide amount to be deposited.")
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
        with open("Files/Accounts.csv", 'r') as file:
            reader = csv.reader(file, delimiter=',')
            a = []
            for i in reader:
                a.append(i)

            for i in a:
                if i[1] == int(pin):
                    speak(f"Your balance is {i[2]}")
                    print(f"Your balance is {i[2]}")

        speak(regards)
        exit()

    # Code for checking balance.

elif "Like to know balance" in said.lower() or "Balance inquiry" in said.lower() or "Balance" in said.lower():
    speak("You have selected to check your balance.")
    with open("Files/Accounts.csv", 'r') as file:
        reader = csv.reader(file, delimiter=',')
        a = []
        for i in reader:
            a.append(i)

        for i in a:
            if i[1] == int(pin) and i[3] == accountNumber:
                speak(f"Your balance is: {i[2]}")
                print(f"Your balance is: {i[2]}")


# Code fir changing pin

elif "i would like to change my pin" in said.lower() or "change pin" in said.lower():

    speak("You have chosen to change your pin, please enter your old pin.")
    print("Please enter your old pin: ")
    tries = 0
    f = 1
    while f == 1:
        oldPin = getpass_asterisk.getpass()
        if int(oldPin) != int(pin):
            speak("Your pin does not match, please enter your old pin again.")
            print("Your pin does not match, please enter your new pin again:")
            tries = tries + 1
            if tries == 3:
                speak("You have exceeded the maximum number of trials.")
                exit()
        else:
            pinTrials = 0
            while f == 1:
                speak("Enter your new pin.")
                print("Enter your new pin:")
                newPin1 = getpass_asterisk.getpass()
                if newPin1.isdigit() and len(newPin1) == 4:
                    speak("Please, re-enter your new pin to confirm.")
                    print("Please, re-enter your new pin to confirm:")
                    newPin2 = getpass_asterisk.getpass()
                    if newPin2.isdigit() and len(newPin2) == 4:
                        # Pin verification
                        if newPin1 == newPin2:
                            with open("Files/Accounts.csv", 'r') as file:
                                reader = csv.reader(file, delimiter=',')
                                l = []
                                for i in reader:
                                    l.append(i)
                                for i in l:
                                    i[1] = int(i[1])
                                    i[2] = float(i[2])
                                    # Wrong pin can only be entered at most, 3 times.
                                    if i[1] == int(oldPin) and i[3] == accountNumber:
                                        i[1] == int(newPin1)  # More than 3 entries will cause system exit
                                        f == 0

                                        speak("Your new pin has been set successfully!")
                                        print("Your new pin has been set successfully!")
                                        speak(regards)
                            file = open("Files/Accounts.csv", 'w',
                                        newline='')
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
