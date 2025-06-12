import csv
import datetime
import os
import platform
from colorama import Fore, Style, init
import sys
import termios
import tty

init()

def play_sound(choice):
    if choice == 'A':
        os.system('afplay A.m4a &')
    elif choice == 'B':
        os.system('afplay B.m4a &')

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        print(ch, end="", flush=True)
        if ord(ch) == 27:  # ESC key
            return 'ESC'
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def ask_dice_proportions():
    while True:
        proportions = input("Enter dice proportions (e.g., 60:40): ").strip()
        if proportions:
            return proportions.replace(" ", "_").replace(":", "_")
        print(Fore.RED + "Invalid input. Please enter a valid dice proportion." + Style.RESET_ALL)

def ask_dice_result(throw_id):
    while True:
        print(f"Throw {throw_id} (A for big, B for small): ", end="", flush=True)
        key = get_key().upper()
        print()  # move to new line
        if key == 'A' or key == 'B':
            play_sound(key)
            return key
        elif key == 'ESC':
            return 'ESC'
        print(Fore.RED + "Invalid input. Only 'A' (big), 'B' (small), or ESC to correct." + Style.RESET_ALL)

def main():
    proportions = ask_dice_proportions()
    filename = f"diceroll_{proportions}.csv"
    file_exists = os.path.isfile(filename)

    data = []
    if file_exists:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            data = list(reader)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Result", "Timestamp"])

        current_id = len(data)
        for row in data:
            writer.writerow(row)

        while current_id < 500:
            result = ask_dice_result(current_id + 1)
            if result == 'ESC':
                if current_id > 0:
                    current_id -= 1
                    data.pop()
                    file.seek(0)
                    file.truncate()
                    writer.writerow(["ID", "Result", "Timestamp"])
                    for i, row in enumerate(data):
                        writer.writerow([i, row[1], row[2]])
                continue

            timestamp = datetime.datetime.now().isoformat()
            writer.writerow([current_id, result, timestamp])
            file.flush()
            os.fsync(file.fileno())
            data.append([current_id, result, timestamp])
            current_id += 1

    print("Progress finished.")

if __name__ == "__main__":
    main()
