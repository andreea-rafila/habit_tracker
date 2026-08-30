import json
from datetime import date, timedelta
from colorama import Fore, Style, init
init(autoreset=True)

DATA_FILE = "habits.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"habits": ["Study", "Gym", "Self-care"], "log": {}}

    data.setdefault("best_streaks", {})
    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def check_in(data):
    today = str(date.today())
    done_today = data["log"].get(today, [])

    print(f"\nToday is {today}")

    habits = data["habits"]
    history = [] # our stack: stores (habit, was_added) pairs
    i = 0
    while i < len(habits):
        habit = habits[i]
        if habit in done_today:
            print(f" [x] {habit} (already logged)")
            i += 1
            continue
        answer = input(f"  Did you do '{habit}' today? (y/n, or 'u' for undo): ").strip().lower()

        if answer == "u":
            if not history:
                print(Fore.YELLOW + "Nothing to undo.\n")
                continue
            last_habit, was_added = history.pop()
            if was_added:
                done_today.remove(last_habit)
            i -= 1
            print(Fore.YELLOW + f"  Undid '{last_habit}'.\n")
            continue

        if answer == "y":
            done_today.append(habit)
            history.append((habit, True))
        else:
            history.append((habit, False))
        i += 1

    confirm = input("Press Enter to save, or 'u' to undo the last answer: ").strip().lower()
    if confirm == "u" and history:
        last_habit, was_added = history.pop()
        if was_added:
            done_today.remove(last_habit)
        print(f"  Undid '{last_habit}'.\n")
        answer = input(f"  Did you do '{last_habit}' today? ").strip().lower()
        if answer == "y":
            done_today.append(last_habit)

    data["log"][today] = done_today
    save_data(data)
    update_best_streaks(data)
    save_data(data)
    print(Fore.GREEN + "Saved today's progress!\n")

def update_best_streaks(data):
    for habit in data["habits"]:
        current = show_streak(data, habit)
        best = data["best_streaks"].get(habit, 0)
        data["best_streaks"][habit] = max(current, best)

def show_streak(data, habit):
    streak = 0
    day = date.today()
    while True:
        day_str = str(day)
        if habit in data["log"].get(day_str, []):
            streak += 1
            day -= timedelta(days=1)
        else:
            break
    return streak

def view_stats(data):
    print("\n--- Current Streaks ---")
    for habit in data["habits"]:
        streak = show_streak(data, habit)
        best = data["best_streaks"].get(habit, 0)
        week = weekly_view(data, habit)
        print(f" {habit}: {week} ({streak} day streak, best: {best})")
    print()

def add_habit(data):
    new_habit = input("Enter new habit: ").strip()
    if new_habit == "":
        print(Fore.RED + "Habit name can't be empty.\n")
        return
    if new_habit in data["habits"]:
        print(Fore.RED + f"'{new_habit}' is already being tracked.\n")
        return
    data["habits"].append(new_habit)
    save_data(data)
    print(Fore.GREEN + f"Added '{new_habit}'!\n")

def remove_habit(data):
    if not data["habits"]:
        print("No habits to remove.\n")
        return

    print("\nYour habits:")
    for i, habit in enumerate(data["habits"], start=1):
        print(f" {i}) {habit}")

    choice = input("Enter to remove (or 0 to cancel): ").strip()
    if choice == "0":
        print("Cancelled.\n")
        return

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(data["habits"]):
        print(Fore.RED + "Invalid choice.\n")
        return

    index = int(choice) - 1
    removed = data["habits"].pop(index)
    save_data(data)
    print(Fore.GREEN + f"Removed '{removed}'.\n")

def list_habits(data):
    if not data["habits"]:
        print("No habits tracked yet.\n")
        return

    for i, habit in enumerate(data["habits"], start=1):
        print(f" {i}) {habit}")
    print()

def weekly_view(data, habit):
    symbols = []
    day = date.today()
    for _ in range(7):
        day_str = str(day)
        if habit in data["log"].get(day_str, []):
            symbols.append(Fore.GREEN + "✓")
        else:
            symbols.append(Fore.RED + "x")
        day -= timedelta(days=1)
    symbols.reverse()
    return " ".join(symbols) + Style.RESET_ALL

def main():
    data = load_data()
    while True:
        print("1) Check in for today")
        print("2) View streaks")
        print("3) View habits")
        print("4) Add a habit")
        print("5) Remove a habit")
        print("6) Quit")
        choice = input("> ").strip()

        if choice == "1":
            check_in(data)
        elif choice == "2":
            view_stats(data)
        elif choice == "3":
            list_habits(data)
        elif choice == "4":
            add_habit(data)
        elif choice == "5":
            remove_habit(data)
        elif choice == "6":
            break
        else:
            print("Not a valid option, try again.\n")

if __name__ == "__main__":
    main()