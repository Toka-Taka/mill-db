import re

END = '\000'

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
        self.program = COMMENT.sub('', program)  # Чистим комментарии
        self.pos = 0
        self.col = 1
        self.line = 1

    @property
    def char(self):
        return self.program[self.pos] if self.pos == len(self.program) else END

    def next(self):
        if self.char == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        self.pos = self.pos + 1 if self.pos < len(self.program) else self.pos

    def __str__(self):
        return "<{}:{}>".format(self.line, self.col)

    def __sub__(self, other):
        return "<{}:{}> - <{}:{}>".format(other.line, other.pos, self.line, self.pos)


def lexer(p: Pos):
    while p.char != END:
        while p.char in WHITESPACE:
            p.next()

        if p.char in "();,=":
            yield 'SYMBOLS', SYMBOLS[p.char], p.char
            p.next()
            continue

        elif p.char in "<>":
            c1 = p.char
            p.next()
            c2 = c1 + p.char
            if c2 in ("<>", "<=", ">="):
                yield 'SYMBOLS', SYMBOLS[c2], c2
                p.next()
            else:
                yield 'SYMBOLS', SYMBOLS[c1], c1
            continue

        if '1' <= p.char <= '9':
            buf = ''
            while '0' <= p.char <= '9':
                buf += p.char
                p.next()
            yield 'INTEGER', int(buf), buf
            continue
        is_param = p.char == '@' and (p.next() or True)
        if 'a' <= p.char <= 'z' or 'A' <= p.char <= 'Z':
            buf = ''
            while 'a' <= p.char <= 'z' or 'A' <= p.char <= 'Z' or '0' <= p.char <= '9' or p.char == '_':
                buf += p.char
                p.next()
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
        #  todo: Exception wrong symbol

