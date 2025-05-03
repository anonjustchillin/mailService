class User:
    def __init__(self, name, role):
        self.name = name if name is not None else None
        self.role = role if role is not None else None

    def __repr__(self) -> str:
        return f'({self.name}, {self.role})'
