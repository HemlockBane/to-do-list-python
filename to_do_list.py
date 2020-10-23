from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime

db_file_name = "todo.db"
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