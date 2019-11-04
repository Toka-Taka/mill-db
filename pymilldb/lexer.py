import re

END_CHAR = '\000'

SYMBOLS = {
    "(": "LPARENT",
    ")": "RPARENT",
    ";": "SEMICOLON",
    ",": "COMMA",
    "=": "EQ",
    "<": "LESS",
    ">": "MORE",
    "<>": "NOT_EQ",
    "<=": "LESS_OR_EQ",
    ">=": "MORE_OR_EQ",
}

KEYWORDS = {
    "table": "TABLE",
    "join":  "JOIN",

    "sequence": "SEQUENCE",
    "nextval": "NEXTVAL",
    "currval": "CURRVAL",

    "create": "CREATE",
    "pk": "PK",

    "select": "SELECT",
    "from": "FROM",
    "where": "WHERE",

    "insert": "INSERT",
    "values": "VALUES",

    "procedure": "PROCEDURE",
    "begin": "BEGIN",
    "in": "IN",
    "out": "OUT",
    "set": "SET",

    "index": "INDEX",
    "on": "ON",

    "and": "AND",
    "or": "OR",
    "not": "NOT",
}

TYPES = {
    "int": "INT",
    "float": "FLOAT",
    "double": "DOUBLE",
    "char": "CHAR",
    'text': 'TEXT',
}

IDENTIFIER = re.compile(r'[A-Za-z][A-Za-z0-9_]*')
PARAMETER = re.compile(r'@[A-Za-z][A-Za-z0-9_]*')
INTEGER = re.compile(r'([1-9][0-9]*|0)')
# Так как мы не используем флаг re.S (single line),
# то комментарий будет искаться только в пределах одной стоки
COMMENT = re.compile(r'--.*')
WHITESPACE = ' \t\n'


class Pos(object):
    def __init__(self, program: str):
        self.program = program  # Чистим комментарии
        self.pos = 0
        self.col = 1
        self.line = 1

    @property
    def char(self):
        return self.program[self.pos] if self.pos == len(self.program) else END_CHAR

    def next(self):
        if self.char == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        self.pos = self.pos + 1 if self.pos < len(self.program) else self.pos

    def isdecimal(self):
        return self.char.isdecimal()

    def islower(self):
        return self.char.islower()

    def isupper(self):
        return self.char.isupper()

    def isspace(self):
        return self.char.isspace()

    def __str__(self):
        return "<{}:{}>".format(self.line, self.col)

    def __sub__(self, other):
        return "<{}:{}> - <{}:{}>".format(other.line, other.pos, self.line, self.pos)


class Lexer(object):

    def __init__(self, text):
        self.orig_text = text
        self.text = COMMENT.sub('', text)  # Чистим комментарии
        self.pos = Pos(self.text)
        self.__gen_lex = self.__lex()
        self.cur_token, self.cur_value, self.cur_raw_value = next(self.__gen_lex)

    def next(self):
        self.cur_token, self.cur_value, self.cur_raw_value = next(self.__gen_lex)

    def __lex(self):
        while self.pos.char != END_CHAR:
            # Пропускаем пробелы
            while self.pos.isspace():
                self.pos.next()

            # Проверка на спецсимвол длины 1
            if self.pos.char in "();,=":
                yield 'SYMBOLS', SYMBOLS[self.pos.char], self.pos.char
                self.pos.next()
                continue
            # Проверка на спецсимвол длины 2
            if self.pos.char in "<>":
                c1 = self.pos.char
                self.pos.next()
                c2 = c1 + self.pos.char
                if c2 in ("<>", "<=", ">="):
                    yield 'SYMBOLS', SYMBOLS[c2], c2
                    self.pos.next()
                else:
                    yield 'SYMBOLS', SYMBOLS[c1], c1
                continue
            # Проверка на число
            if self.pos.isdecimal():
                buf = ''
                while self.pos.isdecimal():
                    buf += self.pos.char
                    self.pos.next()
                yield 'INTEGER', int(buf), buf
                continue
            # Проверка на параметр/идентификатор
            is_param = self.pos.char == '@' and (self.pos.next() or True)
            if self.pos.islower() or self.pos.isupper():
                buf = ''
                while (
                        self.pos.islower() or
                        self.pos.isupper() or
                        self.pos.isdecimal() or
                        self.pos.char == '_'
                ):
                    buf += self.pos.char
                    self.pos.next()
                if is_param:
                    yield 'PARAMETER', buf, '@'+buf
                else:
                    keyword = KEYWORDS.get(buf.lower())
                    kind = TYPES.get(buf.lower()) if not keyword else None
                    yield (
                        ('KEYWORD', keyword, buf)
                        if keyword else
                        ('TYPE', kind, buf)
                        if kind else
                        ('IDENTIFIER', buf, buf)
                    )
                continue
            #  todo: Exception processing
        while True:
            yield 'END', END_CHAR, END_CHAR
