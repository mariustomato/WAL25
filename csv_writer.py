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
    file_name = "S.m4a" if choice == 'B' else "S.m4a"
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    if os.path.isfile(file_path):
        os.system(f'afplay "{file_path}" &')
    else:
        print(Fore.RED + f"Audio file not found: {file_path}" + Style.RESET_ALL)

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
        print(f"Throw {throw_id}: ", end="", flush=True)
        key = get_key().upper()
        print()  # move to new line
        if key in ['B', 'S']:
            play_sound(key)
            return key
        elif key == 'ESC':
            return 'ESC'
        elif key == 'X':
            return 'EXIT'
        print(Fore.RED + "Invalid input. Use: B = BIG, S = SMALL, X = Exit, ESC = Previous Input." + Style.RESET_ALL)

def main():
    proportions = ask_dice_proportions()
    print("B = BIG, S = SMALL, X = Exit, ESC = Previous Input")
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_path, "data")
    os.makedirs(data_dir, exist_ok=True)
    filename = os.path.join(data_dir, f"diceroll_{proportions}.csv")
    file_exists = os.path.isfile(filename)

    try:
        data = []
        if file_exists:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                data = list(reader)

        current_id = len(data)
        while current_id < 500:
            result = ask_dice_result(current_id + 1)
            if result == 'EXIT':
                print(Fore.YELLOW + "Exit command received. Exiting program." + Style.RESET_ALL)
                break
            elif result == 'ESC':
                if current_id > 0:
                    current_id -= 1
                    data.pop()
                continue

            timestamp = datetime.datetime.now().isoformat()
            data.append([str(current_id), result, timestamp])
            current_id += 1

            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Result", "Timestamp"])
                for row in data:
                    writer.writerow(row)
                file.flush()
                os.fsync(file.fileno())

        if current_id >= 500:
            print("Progress finished.")
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nProgram interrupted by user. Exiting." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
