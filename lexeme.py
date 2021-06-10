class Lexeme:
    def __init__(self, identifier, number, content, priority=None):
        self.identifier = identifier
        self.number = number
        self.content = content
        self.priority = priority

    def __str__(self):
        # return self.identifier + str(self.number)
        return self.content
