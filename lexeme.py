class Lexeme:
    def __init__(self, identifier, number, content):
        self.identifier = identifier
        self.number = number
        self.content = content

    def __str__(self):
        return self.identifier + str(self.number)
