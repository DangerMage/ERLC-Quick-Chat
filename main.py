import yaml
import keyboard as kb
import os
import time
from ahk import AHK

ahk = AHK()


files = []
path = ""

for file in os.listdir("profiles"):
    if os.path.isdir(file):
        continue
    else:
        files.append(file)

if len(files) > 1:
    inputLoop = True
    while inputLoop:
        choice = input("Multiple profiles found. Please select one (.yaml ignored. Don't add it):\n" + "\n".join(files) + "\n")
        if files.__contains__(choice + ".yaml"):
            print(choice)
            inputLoop = False
            path = "profiles/" + choice + ".yaml"
        else:
            print("Not a profile. Please try again:\n")
else:
    path = "profiles/" + files[0]

os.system('cls')
print("Loaded profile: ", path, "\nPress 'End' to end the program\nQuick Chats:\n")

with open(path) as profile:
    quickChats = yaml.safe_load(profile)


def sendMessage(message, number):
    ahk.key_press('/')
    time.sleep(0.1)
    ahk.type(message)
    time.sleep(0.1)
    ahk.key_press('Enter')


def sendRadio(message, number):
    ahk.key_press('t')
    time.sleep(0.1)
    sendMessage(message, number)


for keybind, message in quickChats.items():
    if message[0] == "@":
        correctMessage = message[1:]
        kb.add_hotkey(keybind, sendRadio, args=(f"{correctMessage}", 0.1))
        print(f"\nKeybind: {keybind} Message: {correctMessage}, (radio message)")
    else:
        kb.add_hotkey(keybind, sendMessage, args=(f"{message}", 0.1))
        print(f"\nKeybind: {keybind} Message: {message}")

kb.wait("end")

kb.unhook_all()
