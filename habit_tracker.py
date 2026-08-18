import json
from datetime import date, timedelta

DATA_FILE = "habits.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"habits": ["Study", "Gym", "Self-care"], "log": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def check_in(data):
    today = str(date.today())
    done_today = data["log"].get(today, [])

    print(f"\nToday is {today}")
    for habit in data["habits"]:
        if habit in done_today:
            print(f"  [x] {habit} (already logged)")
            continue
        answer = input(f"  Did you do '{habit}' today? (y/n): ").strip().lower()
        if answer == "y":
            done_today.append(habit)
    data["log"][today] = done_today
    save_data(data)
    print("Saved today's progress!\n")

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
        print(f" {habit}: {streak} day streak")
    print()

def add_habit(data):
    new_habit = input("Enter new habit: ").strip()
    if new_habit == "":
        print("Habit name can't be empty.\n")
        return
    if new_habit in data["habits"]:
        print(f"'{new_habit}' is already being tracked.\n")
        return
    data["habits"].append(new_habit)
    save_data(data)
    print(f"Added '{new_habit}'!\n")

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

    if not choice.isdigit() or int(choice) < 0 or int(choice) > len(data["habits"]):
        print("Invalid choice.\n")
        return

    index = int(choice) - 1
    removed = data["habits"].pop(index)
    save_data(data)
    print(f"Removed '{removed}'.\n")

def list_habits(data):
    if not data["habits"]:
        print("No habits tracked yet.\n")
        return

    for i, habit in enumerate(data["habits"], start=1):
        print(f" {i}) {habit}")
    print()

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