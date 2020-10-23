# Nothing important here.... Just a place to experiment and try out stuff




# 1. Today's tasks (Prints all tasks for today) ...Probably from the db
# 2. Add task (Asks for task description and saves it into the db)
# 0. Exit.

# Db structure:
# - db file: todo.db
# - table name: task
# - Columns include:
# -- id (integer type, primary key)
# -- task (string)
# -- deadline (date, default is today())


# Today's tasks
# Gets all tasks from db
# Prints "Today"
# If tasks don't exist, print("Nothing to do!")
# If tasks exist, print the tasks enumerated and on a new linw


# Add task
# Prints "Enter task"
# Accepts task from user input
# Prints "The task has been added!"

# Exit
# Prints "Bye!"


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime

db_file_name = "todo.s3db"
engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

    # def __str__(self):
    #     return f"task_name: {self.task}, deadline: {self.deadline}"

Base.metadata.create_all(engine)



class ToDoList:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def get_all_tasks(self):
        rows = self.session.query(Task).all()
        return rows


    def add_task(self, Task):
        self.session.add(Task)
        self.session.commit()

    def run(self):
        while True:
            print("1) Today's tasks", "2) Add task", "0) Exit", sep="\n")
            user_input = input()

            if user_input == "0":
                print("Bye!")
                break
            elif user_input == "1":
                print("Today:")

                tasks = self.get_all_tasks()
                if len(tasks) == 0:
                    print("Nothing to do!")
                for idx, task in enumerate(tasks):
                    print(f"{idx + 1}.", task)

            elif user_input == "2":
                task = input("Enter task:\n")
                self.add_task(Task(task=task))
                print("The task has been added!")


to_do_list = ToDoList()
to_do_list.run()
# to_do_list.get_all_tasks()
