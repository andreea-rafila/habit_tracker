import json
from datetime import date, timedelta

DATA_FILE = "habits.json"
DEFAULT_HABITS = ["Study", "Gym", "Self-care"]

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def check_in(data):
    today = str(date.today())
    done_today = data.get(today, [])

    print(f"\nToday is {today}")
    for habit in DEFAULT_HABITS:
        if habit in done_today:
            print(f"  [x] {habit} (already logged)")
            continue
        answer = input(f"  Did you do '{habit}' today? (y/n): ").strip().lower()
        if answer == "y":
            done_today.append(habit)
    data[today] = done_today
    save_data(data)
    print("Saved today's progress!\n")

def show_streak(data, habit):
    streak = 0
    day = date.today()
    while True:
        day_str = str(day)
        if habit in data.get(day_str, []):
            streak += 1
            day -= timedelta(days=1)
        else:
            break
    return streak

def view_stats(data):
    print("\n--- Current Streaks ---")
    for habit in DEFAULT_HABITS:
        streak = show_streak(data, habit)
        print(f" {habit}: {streak} day streak")
    print()

def main():
    data = load_data()
    while True:
        print("1) Check in for today")
        print("2) View streaks")
        print("3) Quit")
        choice = input("> ").strip()

        if choice == "1":
            check_in(data)
        elif choice == "2":
            view_stats(data)
        elif choice == "3":
            break
        else:
            print("Not a valid option, try again.\n")

if __name__ == "__main__":
    main()