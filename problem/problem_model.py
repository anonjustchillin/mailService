class Problem:
    def __init__(self, title, progress):
        self.title = title
        self.progress = progress if progress is not None else None

    def __str__(self):
        return f'({self.title}, {self.progress})'
