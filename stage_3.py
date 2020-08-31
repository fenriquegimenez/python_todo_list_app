from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta

# initialising the parent class for a table
Base = declarative_base()


# a task table
class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        """
        it will look like this format
        id. task
        id. task
        id. task
        """
        return f"{self.id}. {self.task}"


class To_Do_List:
    prompt = "1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Add task\n0) Exit\n"

    def __init__(self, db_name):
        """
        initialising the database and gui
        """
        # table and database initialising
        self.engine = create_engine(f"sqlite:///{db_name}.db?check_same_thread=False")
        Base.metadata.create_all(self.engine)

        # Session and interaction with database initialising
        self.session = sessionmaker(bind=self.engine)()

        # todo list gui initialising
        self.choices = {'1': self.show_today_tasks, '2': self.show_week_tasks, '3': self.show_all_tasks,
                        '4': self.add_task, '0': self.shutdown}
        self.running = True
        self.main()

    def shutdown(self):
        """
        shuts down the program, by terminating the while loop
        """
        self.running = False
        print('Bye!')

    def show_today_tasks(self):
        """
        acquires all the records in the database

        if there are no tasks:
            it will prompt it

        if there are tasks:
            it will print them one by one, in an appropriate format
        """
        date_today = datetime.today()
        month = date_today.strftime('%b')
        day = date_today.day

        tasks = self.session.query(Task).filter(Task.deadline == date_today.date()).all()
        print(f"Today {day} {month}:")
        if tasks:
            for task in tasks:
                print(task)
        else:
            print("Nothing to do!")

    def add_task(self):
        """
        adds a task to the database, with the deadline specified
        """
        task = input('Enter task\n')
        deadline = datetime.strptime(input('Enter deadline\n'), r'%Y-%m-%d')
        self.session.add(Task(task=task, deadline=deadline))
        self.session.commit()
        print("The task has been added!")

    def show_week_tasks(self):
        """
        shows the tasks for this week

        prints in the FORMAT:
        week_day day month:
        1. task
        2. task

        or

        week_day day month:
        Nothing to do!
        """
        for date in (datetime.today() + timedelta(n) for n in range(7)):
            day = date.day
            day_name = date.strftime("%A")
            month = date.strftime('%b')
            tasks = self.session.query(Task).filter(Task.deadline == date.date()).all()
            print(f"{day_name} {day} {month}:")
            if tasks:
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task.task}")
            else:
                print("Nothing to do!")
            print()

    def show_all_tasks(self):
        """
        Shows every task.

        prints in the FORMAT:
        "id. task. day month"
        "1. check tv. 29 Aug"
        """
        print("All tasks:")
        tasks = self.session.query(Task).order_by(Task.deadline).all()
        if tasks:
            for task in tasks:
                month = task.deadline.strftime('%b')
                day = task.deadline.day
                print(f"{task.id}. {task.task}. {day} {month}")
        else:
            print("Nothing to do!")

    def main(self):
        """
        continuously runs the program

        the two print statements, are for line breaks, to maintain proper format of CMD Gui
        lambda: None defines a function that does nothing, as such, if wrong input was entered, it would simply go to the next iteration of the while loop
        no line breaks needed after exiting or showing this week tasks
        """
        while self.running:
            choice = input(self.prompt)
            print()
            self.choices.get(choice, lambda: None)()
            print() if choice not in {'0', '2'} else None


To_Do_List('todo')
