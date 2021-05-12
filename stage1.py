from lexeme import Lexeme
from container import Container
from scanner import Scanner


def read_lexemes():
    lexemes = Container()
    build_lexemes("w", lexemes)
    build_lexemes("r", lexemes)
    build_lexemes("o", lexemes)
    return lexemes

def build_lexemes(letter, container, lexemes=None):
    if not lexemes:
        lexemes = open(f"source_lexemes\\{letter}").read().split("\n")
    for i in range(len(lexemes)):
        if lexemes[i] not in container.values():
            container.add(Lexeme(letter, container.count(letter) + 1, lexemes[i]))

def write_table(letter, lexemes):
    file = open(f"tables\\{letter}_table", "w")
    for el in lexemes:
        file.write(f"{str(el)} {el.content}\n")
    file.close()

def form_tables(lexemes):
    identifiers = ["w", "r", "o", "i", "c", "n"]
    for letter in identifiers:
        write_table(letter, lexemes.items(identifier=letter))

def write_code(code):
    file = open("machine_code", "w")
    for line in code:
        file.write(" ".join(line) + "\n")
    file.close


def main():
    scanner = Scanner(read_lexemes())
    code = scanner.scan(open("file").read())
    form_tables(scanner.lexemes)
    write_code(code)


if __name__ == '__main__':
    main()
