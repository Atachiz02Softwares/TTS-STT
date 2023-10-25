# ATM FOR THE VISUALLY IMPAIRED

Undergraduate Final Project:

Libraries used are:

1. pyttsx3
2. pyttsx4
3. random
4. gtts
5. speech_recognition
6. os
7. csv
8. getpass_ak
9. datetime

* The model ATM system is mainly developed to make it accessible for the visually impaired people,
  the code written in python3 mainly uses the libraries: pyttsx3 for speech to voice conversion and
  speech_recognition to use the mic for speech to text, it utilizes the Google's API service for voice recognition.

* The transactions performed are locally stored in a CSV file, there are 5-6 preloaded accounts with pin and account
  numbers and names.

* The model involves cash withdrawal, cash deposit and balance inquiry and pin change functions which are all voice
  controlled and keypad controlled for normal usage.

* All errors have been handled diligently and special security features have been added such as:
    1. Account number has to be 10 digits and the password has to be 4 digits .
    2. A max for 3 illegal entries is allowed and after that the programme will terminate itself.
    3. Any wrong or illegal input wil result in programme termination (similar to a real ATM).
       integrity of each input has been checked and only then accepted.

* A personalized library has been imported for displaying '*' for password input to make it more secure.

* NOTE : THE PROGRAMME REQUIRES A GOOD NETWORK CONNECTION AND A QUIET BACKGROUND FOR SPEECH RECOGNITION.