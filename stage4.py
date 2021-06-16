from stage1 import main as stage_1

def exception(code, token):
    if code == 0:
        raise Exception(f"Syntax Error near '{token}'")
    elif code == 1:
        raise Exception(f"Unbalanced Brackets near '{token}'")
    elif code == 2:
        raise Exception(f"Can't perform operation near '{token}'")
    elif code == 3:
        raise Exception(f"'{token}' is not atomic")


class Syntax:
    def __init__(self, code):
        self.code = code
        self.symbol = None
        self.index = -1

    def scan(self):
        if self.index >= len(self.code):
            exception(0, self.symbol)
        self.index += 1
        self.symbol = self.code[self.index]

    def analysis(self):
        self.scan()
        if self.symbol.content != "PROGRAM":
            exception(0, self.symbol)
        self.scan()
        if self.symbol.identifier != "i":
            exception(0, self.symbol)
        self.scan()
        if self.symbol.content != "\\n":
            exception(0, self.symbol)
        self.scan()
        self.text()
        if self.symbol.content != "END":
            exception(0, self.symbol)
        return True

    def text(self):
        while self.symbol.content != "END":
            if self.symbol.content in ["SUBROUTINE", "FUNCTION"]:
                self.procedure()
            else:
                self.line()

    def line(self):
        if self.symbol.content in ["INTEGER", "REAL", "CHARACTER", "DIMENSION"]:
            self.decl()
        else:
            self.operation()

    def decl(self):
        self.scan()
        if self.symbol.identifier != "i":
            exception(0, self.symbol)
        self.scan()
        if self.symbol.content != "\\n":
            while self.symbol.content != "\\n":
                if self.symbol.content == ",":
                    self.scan()
                    if self.symbol.identifier != "i":
                        exception(0, self.symbol)
                self.scan()
            self.scan()
        else:
            self.scan()

    def operation(self):
        if self.symbol.content == "GOTO":
            self.scan()
            if self.symbol.identifier != "i":
                exception(0, self.symbol)
            self.scan()
            if self.symbol.content != "\\n":
                exception(0, self.symbol)
            self.scan()
        elif self.symbol.content == "CALL":
            self.scan()
            if self.symbol.identifier != "i":
                exception(0, self.symbol)
            self.scan()
            if self.symbol.content != "(":
                exception(0, self.symbol)
            self.scan()
            while self.symbol.content != ")":
                self.operand()
                self.scan()
                if self.symbol.content == ")":
                    self.scan()
                    break
                elif self.symbol.content == ",":
                    self.scan()
            self.scan()
            if self.symbol.content != "\\n":
                exception(0, self.symbol)
        elif self.symbol.content == "IF":
            self.conditional_operator()
        elif self.symbol.content == "DO":
            self.cycle()
        else:
            if self.symbol.identifier != "i":
                exception(0, self.symbol)
            self.scan()
            if self.symbol.content != "=":
                exception(2, self.symbol)
            self.scan()
            self.operand()

    def operand(self):
        if not self.atom():
            exception(3, self.symbol)
        self.scan()
        brackets = 0
        while self.symbol.content not in ["\\n", ","]:
            if self.symbol.content == "(":
                brackets += 1
                self.scan()
            elif self.symbol.content == ")":
                if not brackets:
                    return
                else:
                    brackets -= 1
                    self.scan()
            elif self.symbol.content in ["+", "-", "*", "/", "**"]:
                self.scan()
            elif self.symbol.identifier == "o":
                return
            elif self.atom():
                self.scan()
        if brackets:
            exception(1, self.code[self.index - 1])
        self.scan()

    def atom(self):
        return self.symbol.identifier in ["i", "n", "c"]

    def conditional_operator(self):
        self.scan()
        if self.symbol.content != "(":
            exception(0, self.symbol)
        self.scan()
        self.expression()
        if self.symbol.content != ")":
            exception(0, self.symbol)
        self.scan()
        self.operation()

    def expression(self):
        self.operand()
        if not (self.symbol.identifier == "o" and 6 <= self.symbol.number <= 11):
            exception(0, self.symbol)
        self.scan()
        self.operand()

    def cycle(self):
        self.scan()
        if self.symbol.content != "WHILE":
            exception(0, self.symbol)
        self.scan()
        if self.symbol.content != "(":
            exception(0, self.symbol)
        self.scan()
        self.expression()
        if self.symbol.content != ")":
            exception(0, self.symbol)
        self.scan()
        self.scan()
        self.text()
        if self.symbol.content != "END":
            exception(0, self.symbol)
        self.scan()
        self.scan()

    def procedure(self):
        self.scan()
        if self.symbol.identifier != "i":
            exception(0, self.symbol)
        self.scan()
        if self.symbol.content != "\\n":
            exception(0, self.symbol)
        self.scan()
        self.text()
        if self.symbol.content != "END":
            exception(0, self.symbol)


def main():
    code, lexemes = stage_1()
    eol = lexemes.get_lexeme("\\n")
    code = [item for line in code for item in line + [eol]]
    syntax = Syntax(code)
    print(syntax.analysis())


if __name__ == '__main__':
    main()



