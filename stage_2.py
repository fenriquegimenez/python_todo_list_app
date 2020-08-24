from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime


engine = create_engine(f'sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_task():
    new_task = input('Enter task')
    new_row = Table(task=new_task)
    session.add(new_row)
    session.commit()


def print_tasks():
    print('Today:')
    rows = session.query(Table).all()
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        for row in rows:
            print(row.task)


while True:
    print("""1) Today's tasks\n2) Add task\n0) Exit""")
    option = input()
    if option == '0':
        exit()
    elif option == '1':
        print_tasks()
    elif option == '2':
        add_task()
