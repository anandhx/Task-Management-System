import sqlite3
import os
import time
from datetime import datetime, timedelta

# ANSI for colors
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
RED = "\033[1;31m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

def clear_screen():
    """Clear the console."""
    os.system('cls' if os.name == 'nt' else 'clear')

# --------------------------
# Database Setup
# -------------------------
def initialize_db():
    """SQLite database"""
    try:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            description TEXT NOT NULL,
                            deadline TEXT,
                            status TEXT NOT NULL CHECK(status IN ('pending', 'completed')),
                            priority TEXT NOT NULL CHECK(priority IN ('high', 'medium', 'low')) DEFAULT 'medium'
                        )''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"{RED}Database error: {e}{RESET}")
    conn.close()



# ------------------------------
# Date Validation
# ------------------------------
def validate_date(date_str):
    """Check the date DD-MM-YYYY is valid."""
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return date_str
    except ValueError:
        print(f"{RED}Invalid date format! Use DD-MM-YYYY.{RESET}")
        return None


def add_task(description, deadline=None, priority='medium'):
    """Add a new task """
    if not description.strip():
        print(f"{RED}Error: Task description cannot be empty.{RESET}")
        time.sleep(1)
        return

    if deadline:
        deadline = validate_date(deadline)
        if not deadline:
            time.sleep(1)
            return

    if priority not in ['high', 'medium', 'low']:
        print(f"{YELLOW}Invalid priority! Defaulting to 'medium'.{RESET}")
        priority = 'medium'

    try:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (description, deadline, status, priority) VALUES (?, ?, ?, ?)",(description, deadline, 'pending', priority))
        conn.commit()
        conn.close()
        print(f"{GREEN}Task added successfully!{RESET}")
    except sqlite3.Error as e:
        print(f"{RED}Database error: {e}{RESET}")
    time.sleep(1)

def view_tasks(order_by=None):
    """display all tasks."""

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    query = "SELECT * FROM tasks"
    if order_by in ['deadline', 'status', 'priority']:
        query += f" ORDER BY {order_by} ASC"
    cursor.execute(query)
    tasks = cursor.fetchall()
    conn.close()
    display_tasks(tasks)
    input(f"{CYAN}Press Enter to continue...{RESET}")

def view_pending_tasks():
    """
    Retrieve and display tasks that are  'pending'.
    """
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE status = 'pending'")
    tasks = cursor.fetchall()
    conn.close()
    display_tasks(tasks)
    input(f"{CYAN}Press Enter to continue...{RESET}")

def view_completed_tasks():
    """
    Retrieve and display tasks marked as 'completed'.
    """
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE status = 'completed'")
    tasks = cursor.fetchall()
    conn.close()
    display_tasks(tasks)
    input(f"{CYAN}Press Enter to continue...{RESET}")

def search_tasks(keyword):
    """
    Search by specified keyword in their description.
    """
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE description LIKE ?", (f"%{keyword}%",))
    tasks = cursor.fetchall()
    conn.close()
    display_tasks(tasks)
    input(f"{CYAN}Press Enter to continue...{RESET}")

def update_task(task_id, new_description=None, new_status=None, new_priority=None):
    """Update a task """
    try:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        if new_description:
            cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (new_description, task_id))
        if new_status in ['pending', 'completed']:
            cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        if new_priority in ['high', 'medium', 'low']:
            cursor.execute("UPDATE tasks SET priority = ? WHERE id = ?", (new_priority, task_id))

        conn.commit()
        if cursor.rowcount == 0:
            print(f"{RED}Task not found!{RESET}")
        else:
            print(f"{GREEN}Task updated successfully!{RESET}")
        conn.close()
    except sqlite3.Error as e:
        print(f"{RED}Database error: {e}{RESET}")
    time.sleep(1)

def delete_task(task_id):
    """Delete a task"""
    try:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"{RED}Task not found!{RESET}")
        else:
            print(f"{GREEN}Task deleted successfully!{RESET}")
        conn.close()
    except sqlite3.Error as e:
        print(f"{RED}Database error: {e}{RESET}")
    time.sleep(1)


# ------------------------------
# Due Date Reminders
# ------------------------------
def due_date_reminders():
    """Check for tasks due within the next 24 hrs."""
    try:
        now = datetime.now()
        upcoming = now + timedelta(days=1)
        
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE deadline IS NOT NULL AND status = 'pending'")
        tasks = cursor.fetchall()
        conn.close()

        reminders = []
        for task in tasks:
            try:
                deadline_dt = datetime.strptime(task[2], "%d-%m-%Y")
                if now <= deadline_dt <= upcoming:
                    reminders.append(task)
            except ValueError:
                continue  

        return reminders  # Return list
    except sqlite3.Error as e:
        print(f"{RED}Database error: {e}{RESET}")
        return []

def display_tasks(tasks):
    """
    Display tasks in a neatly formatted table with fixed-width columns.
    """
    if not tasks:
        print(f"{RED}No tasks found.{RESET}")
        return


    headers = ["ID", "Description", "Deadline", "Status", "Priority"]
    col_widths = [4, 30, 12, 10, 10]

    # Create the header
    header_format = " | ".join([f"{{:<{w}}}" for w in col_widths])
    border = "-" * (sum(col_widths) + 3 * (len(col_widths) - 1))
    
    print(f"\n{BLUE}{header_format.format(*headers)}{RESET}")
    print(f"{BLUE}{border}{RESET}")

    row_format = header_format
    for task in tasks:
        task_id, desc, deadline, status, priority = task
        deadline_display = deadline if deadline else "N/A"
        print(f"{YELLOW}{row_format.format(task_id, desc, deadline_display, status, priority)}{RESET}")
    print()


# ------------------------------
# Main Menu and User Interface
# ------------------------------
def main():
    initialize_db()
    
    while True:
        clear_screen()
        due_tasks = due_date_reminders()  # Check if there are due soon tasks
        due_count = len(due_tasks)

        # Display menu
        print(f"{CYAN}================ Task Management System ================\n{RESET}")
        if due_count > 0:
            print(f"{RED}0. You have {due_count} task(s) due soon! Enter 0  to view.{RESET}")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. View Completed Tasks")
        print("5. Search Tasks by Description")
        print("6. Sort Tasks")
        print("7. Update Task")
        print("8. Delete Task")
        print("9. Exit")
        print(f"\n{CYAN}========================================================{RESET}")

        choice = input(f"{CYAN}Enter your choice: {RESET}").strip()

        if choice == "0" and due_count > 0:
            clear_screen()
            print(f"{YELLOW}*** Tasks Due Within 24 Hours ***{RESET}")
            display_tasks(due_tasks)
            input(f"{CYAN}Press Enter to return to the menu...{RESET}")

        elif choice == "1":
            clear_screen()
            print(f"{CYAN}--- Add Task ---{RESET}")
            description = input("Enter task description: ").strip()
            deadline = input("Enter deadline (DD-MM-YYYY) or press Enter to skip: ").strip()
            priority = input("Enter priority (high/medium/low) or press Enter for default (medium): ").strip().lower()
            if priority not in ['high', 'medium', 'low']:
                priority = 'medium'
            add_task(description, deadline if deadline else None, priority)

        elif choice == "2":
            clear_screen()
            print(f"{CYAN}--- All Tasks ---{RESET}")
            view_tasks()

        elif choice == "3":
            clear_screen()
            print(f"{CYAN}--- Pending Tasks ---{RESET}")
            view_pending_tasks()

        elif choice == "4":
            clear_screen()
            print(f"{CYAN}--- Completed Tasks ---{RESET}")
            view_completed_tasks()

        elif choice == "5":
            clear_screen()
            print(f"{CYAN}--- Search Tasks ---{RESET}")
            keyword = input("Enter keyword to search: ").strip()
            search_tasks(keyword)

        elif choice == "6":
            clear_screen()
            print(f"{CYAN}--- Sort Tasks ---{RESET}")
            print("1. Deadline")
            print("2. Status")
            print("3. Priority")
            sort_choice = input("Enter your choice (1/2/3): ").strip()
            sort_option = {"1": "deadline", "2": "status", "3": "priority"}.get(sort_choice)
            if sort_option:
                view_tasks(order_by=sort_option)
            else:
                print(f"{RED}Invalid choice!{RESET}")
                time.sleep(1)

        elif choice == "7":
            clear_screen()
            print(f"{CYAN}--- Update Task ---{RESET}")
            try:
                task_id = int(input("Enter task ID: ").strip())
            except ValueError:
                print(f"{RED}Invalid task ID!{RESET}")
                time.sleep(1)
                continue
            new_description = input("New description (or press Enter to keep): ").strip()
            new_status = input("New status (pending/completed) or press Enter to keep: ").strip().lower()
            new_priority = input("New priority (high/medium/low) or press Enter to keep: ").strip().lower()
            update_task(task_id, new_description, new_status, new_priority)

        elif choice == "8":
            clear_screen()
            print(f"{CYAN}--- Delete Task ---{RESET}")
            try:
                task_id = int(input("Enter task ID to delete: ").strip())
            except ValueError:
                print(f"{RED}Invalid task ID!{RESET}")
                time.sleep(1)
                continue
            delete_task(task_id)

        elif choice == "9":
            print(f"{GREEN}Exiting...{RESET}")
            for _ in range(3):
                print(".", end="", flush=True)
                time.sleep(0.5)
            break

        else:
            print(f"{RED}Invalid choice! Please enter a valid option.{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()