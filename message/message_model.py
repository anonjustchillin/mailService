import datetime


class Message:
    def __init__(self, descript, mssg_type, mssg_date, sender, receiver, problem):
        self.descript = descript if descript is not None else None
        self.mssg_type = mssg_type if mssg_type is not None else 'Проблема'
        self.mssg_date = mssg_date if mssg_date is not None else datetime.datetime.now()
        self.sender = sender
        self.receiver = receiver
        self.problem = problem if problem is not None else None

    def __repr__(self) -> str:
        return f'({self.descript}, {self.mssg_type}, {self.mssg_date}, {self.sender}, {self.receiver}, {self.problem})'
