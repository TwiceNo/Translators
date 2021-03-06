class Container:
    def __init__(self):
        self.content = []

    def add(self, value):
        self.content.append(value)

    def items(self, identifier=None, content=None, priority=None):
        if identifier:
            return [value for value in self.content if value.identifier == identifier]
        elif content:
            return [value for value in self.content if value.content == content]
        elif priority:
            return [value for value in self.content if value.priority == priority]
        else:
            return [value for value in self.content]

    def values(self, identifier=None):
        return [value.content for value in self.items(identifier)]

    def count(self, identifier):
        return len([value for value in self.content if value.identifier == identifier])

    def get_identifier(self, content):
        return str(*self.items(content=content))

    def get_lexeme(self, content):
        return self.items(content=content)[0]

    def get_content(self, identifier):
        return [value.content for value in self.content if str(value) == identifier][0]
