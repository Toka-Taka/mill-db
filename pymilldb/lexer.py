import logging
import re
from copy import copy

logger = logging.getLogger('lexer')

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

# Так как мы не используем флаг re.S (single line),
# то комментарий будет искаться только в пределах одной стоки
COMMENT = re.compile(r'--.*')


class Pos(object):
    def __init__(self, program: str):
        self.program = program  # Чистим комментарии
        self.pos = 0
        self.col = 1
        self.line = 1

    @property
    def char(self):
        return self.program[self.pos] if self.pos < len(self.program) else END_CHAR

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

    def __sub__(self, other):
        return self.program[other.pos: self.pos]

    def __copy__(self):
        new_pos = Pos(self.program)
        new_pos.pos = self.pos
        new_pos.col = self.col
        new_pos.line = self.line
        return new_pos

    def __str__(self):
        return "<{}:{}>".format(self.line, self.col)
    #
    # def __sub__(self, other):
    #     return "<{}:{}> - <{}:{}>".format(other.line, other.pos, self.line, self.pos)


class Lexer(object):

    def __init__(self, text):
        self.orig_text = text
        self.text = COMMENT.sub('', text)  # Чистим комментарии
        self.pos = Pos(self.text)
        self.__gen_lex = self.__lex()
        self.cur_token, self.cur_value, self.cur_raw_value = next(self.__gen_lex)

    def next(self):
        logger.debug('%s %s %s', self.cur_token, self.cur_value, self.cur_raw_value)
        self.cur_token, self.cur_value, self.cur_raw_value = next(self.__gen_lex)

    def __lex(self):
        while self.pos.char != END_CHAR:
            # Пропускаем пробелы
            while self.pos.isspace():
                self.pos.next()

            # Проверка на спецсимвол длины 1
            if self.pos.char in "();,=":
                yield SYMBOLS[self.pos.char], SYMBOLS[self.pos.char], self.pos.char
                self.pos.next()
                continue
            # Проверка на спецсимвол длины 2
            if self.pos.char in "<>":
                c1 = self.pos.char
                self.pos.next()
                c2 = c1 + self.pos.char
                if c2 in ("<>", "<=", ">="):
                    yield SYMBOLS[c2], SYMBOLS[c2], c2
                    self.pos.next()
                else:
                    yield SYMBOLS[c1], SYMBOLS[c1], c1
                continue
            # Проверка на число
            if self.pos.isdecimal():
                start = copy(self.pos)
                while self.pos.isdecimal():
                    self.pos.next()
                number = self.pos - start
                yield 'INTEGER', int(number), number
                continue
            # Проверка на параметр/идентификатор
            is_param = self.pos.char == '@' and (self.pos.next() or True)
            if self.pos.islower() or self.pos.isupper():
                start = copy(self.pos)
                while (
                        self.pos.islower() or
                        self.pos.isupper() or
                        self.pos.isdecimal() or
                        self.pos.char == '_'
                ):
                    self.pos.next()
                identifier = self.pos - start
                if is_param:
                    yield 'PARAMETER', identifier, '@'+identifier
                else:
                    lower = identifier.lower()
                    keyword = KEYWORDS.get(lower)
                    kind = TYPES.get(lower) if not keyword else None
                    yield (
                        (keyword, lower, identifier)
                        if keyword else
                        ('TYPE', kind, identifier)
                        if kind else
                        ('IDENTIFIER', identifier, identifier)
                    )
                continue
            #  todo: Exception processing
        while True:
            yield 'END_CHAR', END_CHAR, END_CHAR
