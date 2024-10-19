# To-Do List Manager

This is a command-line based To-Do List Manager built with Python and SQLite, using SQLAlchemy ORM for database operations. The app allows users to manage their tasks, including adding tasks, viewing tasks (today's tasks, week's tasks, all tasks, and missed tasks), and deleting tasks.

## Features

- View today's tasks
- View all tasks
- View tasks for the week
- View missed tasks
- Add new tasks
- Delete tasks

## Database Structure

- **Database File:** `todo.db`
- **Table:** `task`
- **Columns:**
  - `id` (integer, primary key)
  - `task` (string)
  - `deadline` (date, default is today)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install sqlalchemy
   ```
## Usage
Once you run the program, you will be presented with a menu:

1) Today's tasks: View tasks for today.
2) Week's tasks: View tasks for the next 7 days.
3) All tasks: View all tasks in the database.
4) Missed tasks: View tasks that are overdue.
5) Add task: Add a new task by entering the task name and deadline.
6) Delete task: Remove a task from the list by selecting its number.
0) Exit: Close the application.
   
## Dependencies
- Python 3.x
- SQLAlchemy
