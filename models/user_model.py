class User:
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role

    def __repr__(self) -> str:
        return f'({self.id}, {self.name}, {self.role})'
