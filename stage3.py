from stage2 import main as stage_2
from lexeme import Lexeme


relationships = {".GT.": ">",
                 ".LT.": "<",
                 ".GE.": ">=",
                 ".LE.": "<=",
                 ".NE.": "!=",
                 ".EQ.": "=="}

conform = {"WHILE": "while",
           "RETURN": "return",
           "WRITE": "print"}


class Translator:
    def __init__(self, code, lexemes):
        self.code = code
        self.lexemes = lexemes
        self.stack = []
        self.output = []
        self.arrays = []

    def get_identity(self, a):
        if type(a) == str:
            return a
        if a.identifier in ["n", "c"]:
            return a.content
        if a in self.arrays:
            return f"@{a.content}"
        else:
            return f"${a.content}"

    def translate(self):
        for token in self.code:
            if type(token) == str:
                if token.endswith("НП"):
                    name = self.stack.pop().content
                    self.stack.append(f"sub {name}")
                    self.stack.append("{")
                elif token == "КП":
                    self.stack.append("}")
                elif token.endswith("КО"):
                    var_type = self.stack.pop()
                    var_num = self.stack.pop()
                    for i in range(var_num):
                        element = self.stack.pop()
                        if var_type.content == "DIMENSION" and i % 2 != 0:
                            self.arrays.append(element)
                elif token == "УПЛ":
                    b = self.stack.pop()
                    self.stack.append(f"if ({b})")
                    self.stack.append("{")
                elif token == "БП":
                    label = self.stack.pop()
                    self.stack.append(f"goto {label}")
                elif token.startswith("M") and token.endswith(":"):
                    self.stack.append("}")
                elif token.endswith("Ф"):
                    params = [self.get_identity(self.stack.pop()) for i in range(int(token.split()[0]) - 1)]
                    func = self.stack.pop().content
                    self.stack.append(f"&{func}({', '.join(params[::-1])})")
                elif token == "АЭМ":
                    index = self.get_identity(self.stack.pop())
                    self.stack.append(f"@{self.stack.pop()}[{index}]")
            else:
                if type(token) != Lexeme or not token.priority:
                    self.stack.append(token)
                else:
                    if token in self.lexemes.items():
                        if token.content in relationships.keys():
                            b, a = self.get_identity(self.stack.pop()), self.get_identity(self.stack.pop())
                            self.stack.append(f"{a} {relationships[token.content]} {b}")
                        elif token.identifier == "o":
                            b, a = self.get_identity(self.stack.pop()), self.get_identity(self.stack.pop())
                            if (token.content == "=" 
                                    or a.count(" ") and not a.count("(")
                                    or b.count(" ") and not b.count("(")):
                                self.stack.append(f"{a} {token.content} {b}")
                            else:
                                self.stack.append(f"({a} {token.content} {b})")
                        elif token.content in ["INTEGER", "REAL", "CHARACTER", "DIMENSION"]:
                            self.stack.append(token)
                        elif token.content == "WHILE":
                            self.stack.append("while")
                        elif token.content == "END":
                            self.stack.append("}")
                        elif token.content == "GOTO":
                            self.stack.append(f"goto {self.stack.pop()}")

        level = 0
        perl_code = ""
        for i in range(len(self.stack)):
            if self.stack[i] == "while":
                perl_code += ('\t' * level) + f"{self.stack[i]} ({self.stack[i + 1]})\n"
                self.stack[i + 1] = "{"
                continue
            if self.stack[i] == "}":
                level -= 1
            if (self.stack[i] not in ["}", "{"] and
                    not self.stack[i].startswith("if") and
                    not self.stack[i].startswith("sub")):
                self.stack[i] += ";"
            perl_code += ("\t" * level) + self.stack[i] + "\n"
            if self.stack[i] == "{":
                level += 1
        return perl_code


def main():
    code, lexemes = stage_2()
    # print([str(x) for x in code])
    translate = Translator(code, lexemes)
    print(translate.translate())

if __name__ == "__main__":
    main()
