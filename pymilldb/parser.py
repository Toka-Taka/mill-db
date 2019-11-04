from .lexer import Lexer


class Token(Lexer):
    def __eq__(self, other):
        return self.cur_token == other

    def __rshift__(self, other):
        if self.cur_token == other:
            val = self.cur_value
            self.next()
            return val
        else:
            raise Exception  # todo: Обработка ошибок


class Parser(object):

    def __init__(self, token: Token):
        self.token = token

    def program(self):
        # <program_element_list>
        self.program_element_list()

    def program_element_list(self):
        # <program_element>
        # <program_element_list> <program_element>
        self.program_element()
        if self.token != 'END':
            self.program_element_list()

    def program_element(self):
        # <table_declaration>
        # <procedure_declaration>
        # <sequence_declaration>
        self.token >> 'CREATE'
        if self.token == 'TABLE':
            self.table_declaration()
        elif self.token == 'PROCEDURE':
            self.procedure_declaration()
        elif self.token == 'SEQUENCE':
            self.sequence_declaration()
        raise Exception  # todo

    def table_declaration(self):
        # CREATE TABLE id LPARENT <column_declaration_list> RPARENT SEMICOLON
        self.token.next()  # self.token >> 'TABLE'
        table_name = self.token >> 'IDENTIFIER'
        self.token >> 'LPARENT'
        self.column_declaration_list()
        self.token >> 'RPARENT'
        self.token >> 'SEMICOLON'

    def column_declaration_list(self):
        # column_declaration
        # column_declaration_list COMMA column_declaration
        self.column_declaration()
        if self.token == 'COMMA':
            self.token.next()  # self.token >> 'COMMA'
            self.column_declaration_list()

    def column_declaration(self):
        # id type
        # id type PK
        column_name = self.token >> 'IDENTIFIER'
        column_type = self.token >> 'TYPE'
        if self.token == 'PK':
            self.token.next()  # self.token >> 'PK'

    def procedure_declaration(self):
        # CREATE PROCEDURE id LPARENT <parameter_declaration_list> RPARENT BEGIN <statement_list> END SEMICOLON
        self.token.next()  # self.token >> 'PROCEDURE'
        procedure_name = self.token >> 'IDENTIFIER'
        self.parameter_declaration_list()
        self.token >> 'RPARENT'
        self.token >> 'BEGIN'
        self.statement_list()
        self.token >> 'END'
        self.token >> 'SEMICOLON'

    def parameter_declaration_list(self):
        # <parameter_declaration>
        # <parameter_declaration_list> COMMA <parameter_declaration>
        self.parameter_declaration()
        if self.token == 'COMMA':
            self.token.next()  # self.token >> 'COMMA'
            self.parameter_declaration_list()

    def parameter_declaration(self):
        # pid type <parameter_mode>
        parameter_name = self.token >> 'PARAMETER'
        parameter_type = self.token >> 'TYPE'
        self.parameter_mode()

    def parameter_mode(self):
        # IN
        # OUT
        if self.token == 'IN':
            self.token.next()  # self.token >> 'IN'
        elif self.token == 'OUT':
            self.token.next()  # self.token >> 'OUT'
        raise Exception  # todo

    def statement_list(self):
        # <statement>
        # <statement_list> <statement>
        self.statement()
        if self.token == 'INSERT' or self.token == 'SELECT':
            self.statement_list()

    def statement(self):
        # <insert_statement>
        # <select_statement>
        if self.token == 'INSERT':
            self.insert_statement()
        elif self.token == 'SELECT':
            self.select_statement()
        raise Exception  # todo

    def insert_statement(self):
        # INSERT TABLE id VALUES LPARENT <argument_list> RPARENT SEMICOLON
        self.token.next()  # self.token >> 'INSERT'
        self.token >> 'TABLE'
        table_name = self.token >> 'IDENTIFIER'
        self.token >> 'VALUES'
        self.token >> 'LPARENT'
        self.argument_list()
        self.token >> 'RPARENT'
        self.token >> 'SEMICOLON'

    def argument_list(self):
        # <argument>
        # <argument_list> COMMA <argument>
        self.argument()
        if self.token == 'COMMA':
            self.token.next()  # self.token >> 'COMMA'
            self.argument_list()

    def argument(self):
        # pid
        # CURRVAL LPARENT id RPARENT
        # NEXTVAL LPARENT id RPARENT
        if self.token == 'CURRVAL':
            self.token.next()  # self.token >> 'CURRVAL'
            self.token >> 'LPARENT'
            sequence_name = self.token >> 'IDENTIFIER'
            self.token >> 'RPARENT'
            return
        elif self.token == 'NEXTVAL':
            self.token.next()  # self.token >> 'NEXTVAL'
            self.token >> 'LPARENT'
            sequence_name = self.token >> 'IDENTIFIER'
            self.token >> 'RPARENT'
            return
        parameter_name = self.token >> 'PARAMETER'

    def select_statement(self):
        # SELECT <selection_list> FROM <table_list> WHERE <condition_list> SEMICOLON
        self.token.next()  # self.token >> 'SELECT'
        self.selection_list()
        self.token >> 'FROM'
        self.table_list()
        self.token >> 'WHERE'
        self.condition_list()
        self.token >> 'SEMICOLON'

    def selection_list(self):
        # <selection>
        # <selection_list> COMMA <selection>
        self.selection()
        if self.token == 'COMMA':
            self.token.next()  # self.token >> 'COMMA'
            self.selection_list()

    def selection(self):
        # id SET pid
        column_name = self.token >> 'IDENTIFIER'
        self.token >> 'SET'
        parameter_name = self.token >> 'PARAMETER'

    def table_list(self):
        # <table_list> JOIN id
        # id
        table_name = self.token >> 'IDENTIFIER'
        if self.token == 'JOIN':
            self.token.next()  # self.token >> 'JOIN'
            self.table_list()

    def condition_list(self):
        # <search_cond_not>
        # <search_cond_not> AND <condition_list>
        # <search_cond_not> OR <condition_list>
        # LPARENT <condition_list> RPARENT
        # LPARENT <condition_list> RPARENT AND <condition_list>
        # LPARENT <condition_list> RPARENT OR <condition_list>
        if self.token == 'LPARENT':
            self.token.next()  # self.token >> 'LPARENT'
            self.condition_list()
            self.token >> 'RPARENT'
            if self.token == 'AND':
                self.token.next()  # self.token >> 'AND'
                self.condition_list()
            elif self.token == 'OR':
                self.token.next()  # self.token >> 'OR'
                self.condition_list()
            return
        self.search_cond_not()
        if self.token == 'AND':
            self.token.next()  # self.token >> 'AND'
            self.condition_list()
        elif self.token == 'OR':
            self.token.next()  # self.token >> 'OR'
            self.condition_list()

    def search_cond_not(self):
        # <condition_simple>
        # NOT <condition_simple>
        if self.token == 'NOT':
            self.token.next()  # self.token >> 'NOT'
        self.condition_list()

    def condition_simple(self):
        # id <operator> pid
        # id <operator> id
        pass

    def operator(self):
        # EQ
        # LESS
        # MORE
        # NOT_EQ
        # LESS_OR_EQ
        # MORE_OR_EQ
        pass

    def sequence_declaration(self):
        # CREATE SEQUENCE id SEMICOLON
        self.token >> 'SEQUENCE'
        sequence_name = self.token >> 'IDENTIFIER'
        self.token >> 'SEMICOLON'
