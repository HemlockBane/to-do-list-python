
# Db structure:
# - db file: todo.db
# - table name: task
# - Columns include:
# -- id (integer type, primary key)
# -- task (string)
# -- deadline (date, default is today())


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

db_file_name = "todo.db"
test_db_file_name = "todo.s3db"
engine = create_engine(f'sqlite:///{test_db_file_name}?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


class ToDoList:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_today_tasks(self, date=datetime.today().date()):
        rows = self.session.query(Task).filter(Task.deadline == date).all()
        return rows

    def get_all_tasks(self):
        rows = self.session.query(Task).order_by(Task.deadline).all()
        return rows

    def get_missed_tasks(self):
        rows = self.session.query(Task).filter(Task.deadline < datetime.today().date()).order_by(Task.deadline).all()
        return rows

    def add_task(self, task):
        self.session.add(task)
        self.session.commit()

    def delete_task(self, task):
        self.session.delete(task)
        self.session.commit()

    # def get_week_tasks(self):
    #     today = datetime.today().date()
    #     seven_days_after_today = today + timedelta(days=7)
    #     rows = self.session.query(Task).filter(Task.deadline.between(today, seven_days_after_today)).order_by(
    #         Task.deadline).all()
    #     return rows

    def run(self):
        while True:
            print("1) Today's tasks", "2) Week's tasks",
                  "3) All tasks", "4) Missed tasks", "5) Add task", "6) Delete task", "0) Exit", sep="\n")
            user_input = input()

            if user_input == "0":  # Exit
                print("Bye!")
                break
            elif user_input == "1":  # Today's tasks
                today_date = datetime.today()
                formatted_date = today_date.strftime("%d %b")
                print(f"Today {formatted_date}:")

                tasks = self.get_today_tasks()
                if len(tasks) == 0:
                    print("Nothing to do!")
                for idx, task in enumerate(tasks):
                    print(f"{idx + 1}.", task)

            elif user_input == "2":  # Weeks' tasks
                for i in range(0, 7):
                    day = datetime.today() + timedelta(days=i)
                    formatted_date = day.strftime('%A %d %b')
                    print(formatted_date)

                    tasks = self.get_today_tasks(day.date())
                    if len(tasks) == 0:
                        print("Nothing to do!\n")
                        continue

                    for idx, task in enumerate(tasks):
                        if task.deadline.weekday() == day.weekday():
                            print(f"{idx + 1}. {task}\n")

            elif user_input == "3":  # All tasks
                print("All tasks:")

                tasks = self.get_all_tasks()
                if len(tasks) == 0:
                    print("Nothing to do!")
                    continue
                for idx, task in enumerate(tasks):
                    formatted_date = task.deadline.strftime('%#d %b')
                    print(f"{idx + 1}. {task.task}. {formatted_date}")

            elif user_input == "4":
                print("Missed tasks:")
                tasks = self.get_missed_tasks()
                for idx, task in enumerate(tasks):
                    formatted_date = task.deadline.strftime("%#d %b")
                    print(f"{idx + 1}. {task}. {formatted_date}")

            elif user_input == "5":  # Add task
                task = input("Enter task:\n")
                date_string = input("Enter deadline:\n")
                deadline = datetime.strptime(date_string, "%Y-%m-%d").date()
                self.add_task(Task(task=task, deadline=deadline))
                print("The task has been added!")

            elif user_input == "6":
                print("Choose the number of the task you want to delete:")
                tasks = self.get_all_tasks()
                for idx, task in enumerate(tasks):
                    formatted_date = task.deadline.strftime("%#d %b")
                    print(f"{idx + 1}. {task}. {formatted_date}")

                user_input = int(input())
                selected_task = tasks[user_input - 1]
                self.delete_task(selected_task)
                print("This task has been deleted!")


to_do_list = ToDoList()
to_do_list.run()