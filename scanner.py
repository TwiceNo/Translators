from lexeme import Lexeme
from re import fullmatch
from string import digits, ascii_letters

class Scanner:
    def __init__(self, lexemes):
        self.lexemes = lexemes

    def scan(self, code):
        code = code.split("\n")
        machine_code = []
        for line in code:
            # if line and line[0] != "C":
            machine_code.append(self.translate(line.strip()))
        return machine_code

    def translate(self, line):
        line += " "

        extracted_lexemes = []
        idx_first, idx_last = 0, 0
        is_constant, is_exponent, is_real = False, False, False
        quote_type, lexeme_type = None, None

        for idx_last in range(len(line)):
            if idx_last < idx_first:
                continue

            symbol = line[idx_last]

            if symbol in ["\'", "\""]:
                if lexeme_type:
                    self.raise_exception(2)
                if is_constant and symbol == quote_type:
                    lexeme = line[idx_first:idx_last + 1].strip()
                    if lexeme:
                        extracted_lexemes.append(self.translate_lexeme(lexeme, "c"))
                    idx_first = idx_last + 1
                    quote_type = None
                    is_constant = False
                elif not is_constant and not quote_type:
                    quote_type = symbol
                    is_constant = True

            elif not is_constant:

                if symbol.isalpha():
                    if not lexeme_type:
                        lexeme_type = "alpha"
                    elif lexeme_type == "numeric":
                        if symbol == "E":
                            if is_exponent:
                                self.raise_exception(2)
                            else:
                                is_exponent = True
                        else:
                            self.raise_exception(2)

                elif symbol.isdigit():
                    if not lexeme_type:
                        lexeme_type = "numeric"
                        is_exponent, is_real = False, False

                elif symbol in self.lexemes.values("o") + ["."]:
                    if lexeme_type == "operator":
                        lexeme = line[idx_first:idx_last + 1].strip()
                        if lexeme:
                            extracted_lexemes.append(self.translate_lexeme(lexeme))
                        idx_first = idx_last + 1
                        lexeme_type = None
                    elif symbol == ".":
                        if not lexeme_type:
                            if line[idx_last + 1].isdigit():
                                lexeme_type = "numeric"
                            else:
                                lexeme_type = "operator"
                        elif lexeme_type == "numeric":
                            if is_real:
                                lexeme = line[idx_first:idx_last].strip()
                                if lexeme:
                                    extracted_lexemes.append(self.translate_lexeme(lexeme, 'n'))
                                idx_first = idx_last
                                lexeme_type = "operator"
                            else:
                                is_real = True
                    else:
                        if symbol in ["-", "+"] and is_exponent:
                            is_exponent = False
                            continue
                        lexeme = line[idx_first:idx_last].strip()
                        if lexeme:
                            extracted_lexemes.append(self.translate_lexeme(lexeme))
                        if line[idx_last:idx_last + 2] == "**":
                            lexeme_type = "operator"
                            idx_first = idx_last
                        else:
                            extracted_lexemes.append(self.translate_lexeme(line[idx_last], "o"))
                            lexeme_type = None
                            idx_first = idx_last + 1

                elif symbol in self.lexemes.values('r') + [" "]:
                    lexeme = line[idx_first:idx_last].strip()
                    if lexeme:
                        extracted_lexemes.append(self.translate_lexeme(lexeme))
                    if symbol != " ":
                        extracted_lexemes.append(self.translate_lexeme(line[idx_last], 'r'))
                    lexeme_type = None
                    idx_first = idx_last + 1
        return extracted_lexemes

    def translate_lexeme(self, lexeme, identity=None):
        self.add_lexeme(lexeme, identity)
        return self.lexemes.get_lexeme(lexeme)

    def add_lexeme(self, lexeme, identity=None):
        if lexeme and lexeme not in self.lexemes.values():
            if not identity:
                identity = self.get_identity(lexeme)
            if identity:
                self.lexemes.add(Lexeme(identity, self.lexemes.count(identity) + 1, lexeme))
            else:
                self.raise_exception(1)

    @staticmethod
    def raise_exception(code):
        if code == 1:
            raise Exception("Translation Error")
        elif code == 2:
            raise Exception("Argument Error")
        else:
            raise Exception("Unknown Error")

    @staticmethod
    def get_identity(lexeme):
        if lexeme[0] == lexeme[-1] == "\'" or lexeme[0] == lexeme[-1] == "\"":
            return "c"
        elif lexeme[0].isalpha() and set(lexeme) <= set(ascii_letters + digits + "_"):
            return "i"
        elif fullmatch(r'(\d*\.?\d*(E(\-|\+)?\d+)?)', lexeme):
            return "n"
        return None
