from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

db_file_name = "todo.db"
test_db_file_name = "todo.s3db"
engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False')

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

    def add_task(self, task):
        self.session.add(task)
        self.session.commit()

    def run(self):
        while True:
            print("1) Today's tasks", "2) Week's tasks",
                  "3) All tasks", "4) Add task", "0) Exit", sep="\n")
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
                    break
                for idx, task in enumerate(tasks):
                    formatted_date = task.deadline.strftime('%#d %b')
                    print(f"{idx + 1}. {task.task}. {formatted_date}")

            elif user_input == "4":
                task = input("Enter task:\n")
                date_string = input("Enter deadline:\n")
                deadline = datetime.strptime(date_string, "%Y-%m-%d").date()
                self.add_task(Task(task=task, deadline=deadline))
                print("The task has been added!")


to_do_list = ToDoList()
to_do_list.run()
