# Task Management System

This is a Python-based task management system that allows users to add, view, update, delete, search, and sort tasks.

## Features:
- **Add Task:** Add a new task with a description, deadline, and priority.
- **View Tasks:** View all tasks, view pending tasks, or view completed tasks.
- **Search Tasks:** Search tasks by keywords in their description.
- **Update Tasks:** Update task description, status (pending/completed), or priority.
- **Delete Tasks:** Delete tasks from the system.
- **Sort Tasks:** Sort tasks by deadline, status, or priority.
- **Due Date Reminders:** Remind the user of tasks that are due within the next 24 hours.
- **Task Prioritization:** Allows setting priorities (high, medium, low) for tasks.

## How to Run the Program:
1. **Install Python 3.x:** Make sure Python 3.x is installed on your system.
2. **SQLite3 Database:** SQLite3 is used as the database.
3. **Download the Code:** Clone or download the project files.
4. **Run the Script:** Open a terminal/command prompt and navigate to the directory where the script is located. Then run the script with the following command:
    ```
    python main.py
    ```
   The script will automatically create an SQLite database (`tasks.db`) for storing task information if it doesn’t exist.

## Additional Features:
- **Due Date Reminders:** The program checks for tasks with deadlines and reminds the user about tasks that are due within the next 24 hours.
- **Task Sorting:** You can sort tasks by deadline, status, or priority.
- **Colorful Output:** The program uses ANSI escape codes to provide colorful output in the terminal, making it easier to read and navigate.

## Assumptions and Design Decisions:
- **SQLite Database:** A simple SQLite database is used to store task information. The database contains a table with columns for task description, deadline, status (pending/completed), and priority (high, medium, low).
- **Date Format:** Tasks with deadlines must be entered in the `DD-MM-YYYY` format. The system performs validation to ensure the date is correct.
- **Task Status:** The status of a task can be either `pending` or `completed`.
- **Reminder System:** The program checks for tasks with deadlines and sends reminders for tasks due within the next 24 hours.
- **User Input Handling:** The script prompts the user for inputs through a menu-driven system and validates inputs where necessary.


## Screen Shots 



![image](https://github.com/user-attachments/assets/fca35b4d-f919-499c-bc25-08ae0d8a6919)

![image](https://github.com/user-attachments/assets/d7266655-529e-4b04-abde-131ce9e16a62)
![image](https://github.com/user-attachments/assets/e457d4dc-4e56-4971-8bf2-956d937e7d29)
![image](https://github.com/user-attachments/assets/3a96dd73-0e8b-495c-b2e7-e0635790f1f8)
