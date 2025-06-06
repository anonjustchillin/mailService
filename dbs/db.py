import pyodbc as odbc
from typing import List
import datetime
from models.user_model import User
from models.problem_model import Problem
from models.message_model import Message
import os

DRIVER_NAME = os.environ['DRIVER_NAME']
SERVER_NAME = os.environ['SERVER_NAME']
DATABASE_NAME = os.environ['DATABASE_NAME']

conn = odbc.connect(driver=DRIVER_NAME, server=SERVER_NAME, database=DATABASE_NAME)
c = conn.cursor()


# User
def find_user_id(id: int):
    c.execute('SELECT Id, UserName, UserRole FROM cUser WHERE Id = ?', (id,))

    row = c.fetchone()
    return row


def find_user(name: str):
    c.execute('SELECT Id, UserName, UserRole FROM cUser WHERE UserName = ?', (name,))

    row = c.fetchone()
    return row


def check_user_in_mess(id: int) -> bool:
    c.execute('SELECT COUNT(*) FROM cMessage WHERE cMessage.Sender=? OR cMessage.Receiver=?',
              (id,id))
    count = c.fetchone()[0]
    if count != 0:
        return True
    return False


def insert_user(user: User):
    c.execute('SELECT LAST(Id) FROM cUser')
    last_id = c.fetchone()[0]
    user.id = last_id+1 if last_id else 0

    with conn:
        c.execute('INSERT INTO cUser VALUES (?, ?, ?)',
                  (user.id, user.name, user.role))
        conn.commit()


def delete_user_db(id: int, mess_exist: bool = False):
    c.execute('SELECT COUNT(*) FROM cUser')
    count = c.fetchone()[0]

    with conn:
        if mess_exist:
            c.execute('DELETE FROM cMessage WHERE cMessage.Sender=? OR cMessage.Receiver=?',
                      (id, id))

        c.execute('DELETE FROM cUser WHERE Id=?', (id))
        conn.commit()


def update_user_db(id, name, role):
    with conn:
        if name != "-" and role != "-":
            c.execute('UPDATE cUser SET UserName=?, UserRole=? WHERE Id=?',
                      (name, role, id))
        elif name != "-":
            c.execute('UPDATE cUser SET UserName=? WHERE Id=?',
                      (name, id))
        elif role != "-":
            c.execute('UPDATE cUser SET UserRole=? WHERE Id=?',
                      (role, id))
        conn.commit()


def get_all_users() -> List[User]:
    c.execute('SELECT * FROM cUser')
    res = c.fetchall()
    users = []
    for i in res:
        users.append(User(*i))
    return users


# Problem
def find_problem_id(id: int):
    c.execute('SELECT Id, Title, Progress FROM cProblem WHERE Id = ?', (id,))

    row = c.fetchone()
    return row


def find_problem(title: str):
    c.execute('SELECT Id, Title, Progress FROM cProblem WHERE Title = ?', (title,))

    row = c.fetchone()
    return row


def get_all_problems() -> List[Problem]:
    c.execute('SELECT * FROM cProblem')
    res = c.fetchall()
    problems = []
    for i in res:
        problems.append(Problem(*i))
    return problems


def insert_problem(problem: Problem):
    c.execute('SELECT MAX(Id) FROM cProblem')
    last_id = c.fetchone()[0]
    problem.id = last_id+1 if last_id else 0

    with conn:
        c.execute('INSERT INTO cProblem VALUES (?, ?, ?)',
                  (problem.id, problem.title, problem.progress))
        conn.commit()


def check_problem_in_mess(id: int) -> bool:
    c.execute('SELECT COUNT(*) FROM cMessage WHERE cMessage.Problem=?',
              (id,))
    count = c.fetchone()[0]
    if count != 0:
        return True
    return False


def delete_problem_db(id: int, mess_exist: bool):
    c.execute('SELECT COUNT(*) FROM cProblem')
    count = c.fetchone()[0]

    with conn:
        if mess_exist:
            c.execute('DELETE FROM cMessage WHERE cMessage.Problem=?', 
                      (id))

        c.execute('DELETE FROM cProblem WHERE Id=?', (id))
        conn.commit()


def update_problem_db(id, title, progress):
    with conn:
        if title != "-" and progress != "-":
            c.execute('UPDATE cProblem SET Title=?, Progress=? WHERE Id=?',
                      (title, progress, id))
        elif title != "-":
            c.execute('UPDATE cProblem SET Title=? WHERE Id=?',
                      (title, id))
        elif progress != "-":
            c.execute('UPDATE cProblem SET Progress=? WHERE Id=?',
                      (progress, id))
        conn.commit()


# Message
def send_message(message: Message):
    c.execute('SELECT MAX(Id) FROM cMessage')
    last_id = c.fetchone()[0]
    message.id = last_id+1 if last_id else 0

    with conn:
        c.execute('INSERT INTO cMessage VALUES (?, ?, ?, ?, ?, ?, ?)',
                  (message.id, message.descript, message.mssg_type,
                   message.mssg_date, message.sender, message.receiver, message.problem))
        conn.commit()


def delete_message_db(id):
    c.execute('SELECT COUNT(*) FROM cMessage')
    count = c.fetchone()[0]

    with conn:
        c.execute('DELETE FROM cMessage WHERE Id=?', 
                  (id))
        conn.commit()


def find_message_from_user(id: int, user_id: int):
    c.execute('SELECT * FROM cMessage WHERE cMessage.Id=? AND cMessage.Sender=?',
              (id, user_id))

    row = c.fetchone()
    return row


def get_all_messages_sent(id: int) -> List[Message]:
    c.execute("""SELECT cMessage.Id, cMessage.Descript, cMessage.MssgType, cMessage.MssgDate, cMessage.Sender, cUser.UserName, cProblem.Title
                        FROM cMessage INNER JOIN cProblem ON cMessage.Problem=cProblem.Id
                        INNER JOIN cUser ON cMessage.Receiver=cUser.Id
                        WHERE Sender=?
                        ORDER BY MssgDate DESC""",
              (id,))
    all_mess = c.fetchall()
    messages = []
    for i in all_mess:
        messages.append(Message(*i))

    return messages


def get_all_messages_received(id: int) -> List[Message]:
    c.execute("""SELECT cMessage.Id, cMessage.Descript, cMessage.MssgType, cMessage.MssgDate, cUser.UserName, cMessage.Receiver, cProblem.Title
                        FROM cMessage INNER JOIN cProblem ON cMessage.Problem=cProblem.Id
                        INNER JOIN cUser ON cMessage.Sender=cUser.Id
                        WHERE Receiver=?
                        ORDER BY MssgDate DESC""",
              (id,))
    all_mess = c.fetchall()
    messages = []
    for i in all_mess:
        messages.append(Message(*i))

    return messages
