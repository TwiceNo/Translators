from stage1 import main as stage_1


class Notation:
    def __init__(self, source_code, lexemes):
        self.lexemes = lexemes
        self.source = source_code
        self.stack = []
        self.output = []

    def stack_manipulate(self, param):
        try:
            while self.stack and self.stack[-1].content != param:
                try:
                    self.output.append(self.stack.pop())
                except:
                    exception(0)
        except AttributeError:
            self.output.append(self.stack.pop())
            self.stack_manipulate(param)

    def polish_notation(self):
        operation_counter = []
        label_counter = 1
        procedure_number = 0
        procedure_level = 0
        is_logical_exp = False
        is_function = False
        is_variable = False
        is_cycle = False

        for token in self.source:
            if not token.priority:
                self.output.append(token)
                if (is_function or is_variable) and operation_counter[-1] < 2:
                    operation_counter[-1] += 1
            else:
                if not self.stack:
                    self.stack.append(token)
                    if token.content == "IF":
                        is_logical_exp = True
                    elif token.content == "CALL":
                        is_function = True
                        operation_counter.append(0)
                    elif token.content in ["INTEGER", "REAL", "CHARACTER", "DIMENSION"]:
                        is_variable = True
                        operation_counter.append(0)
                    elif token.content == "END":
                        if self.stack:
                            self.stack.pop()
                        if not is_cycle:
                            self.stack.append("КП")
                            procedure_level -= 1
                        else:
                            self.output.append(token)
                    elif token.content == "PROGRAM":
                        self.stack.pop()
                        procedure_level += 1
                        procedure_number += 1
                        self.stack.append(f"{procedure_level} {procedure_number} НП")
                else:
                    if token.content == "(" or token.content == "[":
                        self.stack.append(token)
                    elif token.content == ")":
                        self.stack_manipulate("(")
                        self.stack.pop()
                        if self.stack[-1].content == "CALL":
                            self.output.append(f"{operation_counter[-1]} Ф")
                            operation_counter.pop()
                            self.stack.pop()
                            is_function = False
                        elif self.stack[-1].content == "IF":
                            self.output.append(f"M{label_counter}")
                            self.output.append(f"УПЛ")
                    elif token.content == "]":
                        self.stack_manipulate("[")
                        self.stack.pop()
                        self.output.append("АЭМ")
                    elif token.content == "CALL":
                        operation_counter.append(0)
                        self.stack.append(token)
                        is_function = True
                    elif token.content == ",":
                        if operation_counter:
                            operation_counter[-1] += 1
                        while self.stack[-1].content not in ["(", "INTEGER", "REAL", "CHARACTER", "DIMENSION"]:
                            try:
                                stack_token = self.stack.pop()
                                self.output.append(stack_token)
                            except:
                                exception(0)
                    elif token.content == "IF":
                        self.stack.append(token)
                        is_logical_exp = True
                    elif token.content == "GOTO":
                        self.output.append("БП")
                    elif token.content == "DO":
                        is_cycle = True
                        self.output.append(token)
                    elif token.content == "WHILE":
                        self.output.append(token)
                    elif token.content == "\\n":
                        if is_logical_exp:
                            self.stack_manipulate("IF")
                            self.output.append(f"M{label_counter}:")
                            self.stack.pop()
                            label_counter += 1
                            is_logical_exp = False
                        elif is_variable:
                            while self.stack[-1].content not in ["INTEGER", "REAL", "CHARACTER", "DIMENSION"]:
                                try:
                                    stack_token = self.stack.pop()
                                    self.output.append(stack_token)
                                except:
                                    exception(0)
                            self.output.append(operation_counter[-1])
                            self.output.append(self.stack.pop())
                            self.output.append(f"{procedure_level} {procedure_number} КО")
                            operation_counter.pop()
                            is_variable = False
                        else:
                            self.stack_manipulate("\\n")
                            if self.stack:
                                self.stack.pop()
                    elif token.content in ["INTEGER", "REAL", "CHARACTER", "DIMENSION"]:
                        operation_counter.append(0)
                        self.stack.append(token)
                        is_variable = True
                    elif token.content == "END":
                        self.stack_manipulate("\\n")
                        self.stack.pop()
                        if not is_cycle:
                            self.stack.append("КП")
                            procedure_level -= 1
                        else:
                            self.output.append(token)
                    elif token.content == "PROGRAM":
                        procedure_level += 1
                        procedure_number += 1
                        self.stack.append(f"{procedure_level} {procedure_number} НП")
                    elif type(self.stack[-1]) == str or self.stack[-1].priority < token.priority:
                        self.stack.append(token)
                    else:
                        while self.stack and self.stack[-1].priority >= token.priority:
                            stack_token = self.stack.pop()
                            self.output.append(stack_token)
                        self.stack.append(token)
        while self.stack:
            stack_item = self.stack.pop()
            if stack_item.content != "\\n":
                self.output.append(stack_item)
        return self.output


def exception(error_code):
    if error_code == 0:
        raise Exception("Syntax Error")


def main():
    code, lexemes = stage_1()
    # for line in code:
    #     print(*list(map(str, line)))
    # print(*[str(x) for line in code for x in line], sep="\n")
    end_of_line = lexemes.get_lexeme("\\n")
    formatted_code = [end_of_line]
    for line in code:
        formatted_code += line + [end_of_line]
    translator = Notation(formatted_code, lexemes)
    # print(" ".join(list(map(str, translator.polish_notation()))))
    return translator.polish_notation(), lexemes
    # for i in range(9):
    #     items = lexemes.items(priority=str(i))
    #     for item in items:
    #         print(item.priority, item.content, str(item), sep="\t")
    #
    #


if __name__ == '__main__':
    main()
