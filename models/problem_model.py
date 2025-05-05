class Problem:
    def __init__(self, id, title, progress):
        self.id = id if id is not None else None
        self.title = title
        self.progress = progress if progress is not None else None

    def __str__(self):
        return f'({self.title}, {self.progress})'
