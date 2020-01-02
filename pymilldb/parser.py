import logging

from . import context
from .lexer import Lexer
from .utils import log

logger = logging.getLogger('parser')


class Token(Lexer):
    def __init__(self, *args, **kwargs):
        super(Token, self).__init__(*args, **kwargs)
        self.is_safe = False

    def __eq__(self, other):
        return self.cur_token == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def safe(self):
        self.is_safe = True
        return self

    def __rshift__(self, other):
        if self.cur_token == other:
            self.is_safe = False
            val = self.cur_value
            self.next()
            return val
        else:
            self.is_safe = False
            if self.is_safe:
                return None
            else:
                raise Exception  # todo: Обработка ошибок


class Parser(object):

    def __init__(self, token: Token):
        self.token = token

    @log(logger)
    def program(self):
        # <program_element_list>
        self.program_element_list()

    @log(logger)
    def program_element_list(self):
        # <program_element>
        # <program_element_list> <program_element>
        self.program_element()
        if self.token != 'END_CHAR':
            self.program_element_list()

    @log(logger)
    def program_element(self):
        # <table_declaration>
        # <procedure_declaration>
        # <sequence_declaration>
        self.token >> 'CREATE'
        if self.token == 'TABLE':
            self.table_declaration()
        # elif self.token == 'PROCEDURE':
        #     self.procedure_declaration()
        # elif self.token == 'SEQUENCE':
        #     self.sequence_declaration()
        else:
            raise Exception  # todo

    @log(logger)
    def table_declaration(self):
        # CREATE TABLE id LPARENT <column_declaration_list> RPARENT SEMICOLON
        self.token.next()  # self.token >> 'TABLE'
        table_name = self.token >> 'IDENTIFIER'
        check_name = context.VARIABLES.get(table_name)
        if check_name:
            logger.error('Table name `%s` is already used for the %s.', table_name, check_name)
            table = context.Table(table_name)
        else:
            table = context.TABLES[table_name] = context.Table(table_name)
            context.VARIABLES[table_name] = 'table'
        self.token >> 'LPARENT'
        self.column_declaration_list(table)
        self.token >> 'RPARENT'
        self.token.safe() >> 'SEMICOLON'

    @log(logger)
    def column_declaration_list(self, table: context.Table):
        # column_declaration
        # column_declaration_list COMMA column_declaration
        self.column_declaration(table)
        if self.token == 'COMMA':
            self.token.next()  # self.token >> 'COMMA'
            self.column_declaration_list(table)

    @log(logger)
    def column_declaration(self, table: context.Table):
        # id type
        # id type PK
        column_name = self.token >> 'IDENTIFIER'
        column_type = self.parse_type()
        is_pk = False
        if self.token == 'PK':
            self.token.next()  # self.token >> 'PK'
            is_pk = True
        table.add_column(context.Column(column_name, column_type, is_pk))

    @log(logger)
    def parse_type(self):
        kind = self.token >> 'TYPE'
        if self.token == 'LPARENT':
            self.token.next()  # self.token >> 'LPARENT'
            size = self.token >> 'INTEGER'
            self.token >> 'RPARENT'
            return context.get_type_by_name(kind, size)
        return context.get_type_by_name(kind)

    @log(logger)
    def procedure_declaration(self):
        # CREATE PROCEDURE id LPARENT <parameter_declaration_list> RPARENT BEGIN <statement_list> END SEMICOLON
        self.token.next()  # self.token >> 'PROCEDURE'
        procedure_name = self.token >> 'IDENTIFIER'
        check_name = context.VARIABLES.get(procedure_name)
        procedure = context.Procedure(procedure_name, 'WRITE')
        if check_name:
            logger.error('Procedure name `%s` is already used for the %s.', procedure_name, check_name)
        else:
            context.VARIABLES[procedure_name] = 'procedure'
            context.PROCEDURES[procedure_name] = procedure
        self.parameter_declaration_list(procedure)
        self.token >> 'RPARENT'
        self.token.safe() >> 'BEGIN'
        statements = self.statement_list(procedure)
        self.token.safe() >> 'END'
        self.token.safe() >> 'SEMICOLON'

    @log(logger)
    def parameter_declaration_list(self, procedure: context.Procedure):
        # <parameter_declaration>
        # <parameter_declaration> (COMMA <parameter_declaration>)*
        self.parameter_declaration(procedure)
        while self.token == 'COMMA':
            self.token.next()  # self.token >> 'COMMA'
            self.parameter_declaration(procedure)

    @log(logger)
    def parameter_declaration(self, procedure: context.Procedure):
        # pid type IN
        # pid type OUT
        parameter_name = self.token >> 'PARAMETER'
        parameter_type = self.parse_type()
        if self.token == 'IN':
            self.token.next()  # self.token >> 'IN'
            parameter = context.InputParameter(parameter_name, parameter_type)
        elif self.token == 'OUT':
            self.token.next()  # self.token >> 'OUT'
            parameter = context.OutputParameter(parameter_name, parameter_type)
            procedure.mode = 'READ'
        else:
            raise Exception  # todo
        procedure.add_parameter(parameter)

    @log(logger)
    def statement_list(self, procedure: context.Procedure):
        # <statement>+
        out = [self.statement(procedure)]
        while self.token == 'INSERT' or self.token == 'SELECT':
            out.append(self.statement(procedure))
        return out

    @log(logger)
    def statement(self, procedure: context.Procedure):
        # <insert_statement>
        # <select_statement>
        if self.token == 'INSERT':
            return self.insert_statement(procedure)
        elif self.token == 'SELECT':
            return self.select_statement(procedure)
        raise Exception  # todo

    @log(logger)
    def insert_statement(self, procedure: context.Procedure):
        # INSERT TABLE id VALUES LPARENT <argument_list> RPARENT SEMICOLON
        self.token.next()  # self.token >> 'INSERT'
        self.token >> 'TABLE'
        table_name = self.token >> 'IDENTIFIER'
        if table_name not in context.TABLES:
            logger.error('Table %s not found', table_name)
        self.token >> 'VALUES'
        self.token >> 'LPARENT'
        arguments = self.argument_list()
        self.token >> 'RPARENT'
        self.token >> 'SEMICOLON'
        return 'INSERT', table_name, arguments

    @log(logger)
    def argument_list(self, procedure: context.Procedure):
        # <argument> (COMMA <argument>)*
        out = [self.argument()]
        while self.token == 'COMMA':
            self.token.next()  # self.token >> 'COMMA'
            out.append(self.argument())
        return out

    @log(logger)
    def argument(self, procedure: context.Procedure):
        # pid
        # CURRVAL LPARENT id RPARENT
        # NEXTVAL LPARENT id RPARENT
        if self.token == 'CURRVAL':
            self.token.next()  # self.token >> 'CURRVAL'
            self.token >> 'LPARENT'
            sequence_name = self.token >> 'IDENTIFIER'
            self.token >> 'RPARENT'
            return 'CURRVAL', sequence_name
        elif self.token == 'NEXTVAL':
            self.token.next()  # self.token >> 'NEXTVAL'
            self.token >> 'LPARENT'
            sequence_name = self.token >> 'IDENTIFIER'
            self.token >> 'RPARENT'
            return 'NEXTVAL', sequence_name
        parameter_name = self.token >> 'PARAMETER'
        return 'PARAMETER', parameter_name

    @log(logger)
    def select_statement(self, procedure: context.Procedure):
        # SELECT <selection_list> FROM <table_list> WHERE <condition_list> SEMICOLON
        self.token.next()  # self.token >> 'SELECT'
        statement = context.SelectStatement()
        self.selection_list(procedure, statement)
        self.token >> 'FROM'
        self.table_list(statement)
        self.token >> 'WHERE'
        conditions = self.condition_list()
        self.token.safe() >> 'SEMICOLON'

    @log(logger)
    def selection_list(self, procedure: context.Procedure, statement: context.SelectStatement):
        # <selection> (COMMA <selection>)*
        self.selection(procedure, statement)
        while self.token == 'COMMA':
            self.token.next()  # self.token >> 'COMMA'
            self.selection(procedure, statement)

    @log(logger)
    def selection(self, procedure: context.Procedure, statement: context.SelectStatement):
        # id SET pid
        column_name = self.token >> 'IDENTIFIER'
        self.token >> 'SET'
        parameter_name = self.token >> 'PARAMETER'
        check_name = procedure.parameters.get(parameter_name)
        if not check_name:
            logger.error('Parameter %s not found in procedure parameters', parameter_name)
        elif not isinstance(check_name, context.OutputParameter):
            logger.error('The parameter %s must be output', parameter_name)
        selection = context.Selection(column_name, parameter_name)
        statement.add_selection(selection)

    @log(logger)
    def table_list(self, statement: context.SelectStatement):
        # id (JOIN id)*
        table_name = self.token >> 'IDENTIFIER'
        check_name = context.TABLES.get(table_name)
        if not check_name:
            logger.error('Table %s not found', table_name)
        else:
            statement.add_table(check_name)
        while self.token == 'JOIN':
            self.token.next()  # self.token >> 'JOIN'
            table_name = self.token >> 'IDENTIFIER'
            check_name = context.TABLES.get(table_name)
            if not check_name:
                logger.error('Table %s not found', table_name)
            else:
                statement.add_table(check_name)

    @log(logger)
    def condition_list(self, procedure: context.Procedure, statement: context.Statement):
        # <condition_simple> (OR|AND <condition_simple>)*
        cond = self.condition_simple()
        interim_out = [[cond]]
        while True:
            if self.token == 'AND':
                self.token.next()  # self.token >> 'AND'
                interim_out[-1].append(self.condition_simple)
            elif self.token == 'OR':
                self.token.next()  # self.token >> 'OR'
                interim_out.append([self.condition_simple])
            else:
                break
        out = (
            ('OR', *map(lambda x: x[0] if len(x) == 1 else ('AND', *x), interim_out))
            if len(interim_out) > 1 else
            ('AND', *interim_out[0])
            if len(interim_out[0]) > 1 else
            interim_out[0][0]
        )
        return out

    @log(logger)
    def condition_simple(self, procedure: context.Procedure, statement: context.Statement):
        if self.token == 'LPARENT':
            self.token.next()  # self.token >> 'LPARENT'
            cond = self.condition_list()
            self.token >> 'RPARENT'
        elif self.token == 'NOT':
            self.token.next()  # self.token >> 'NOT'
            cond = ('NOT', self.condition_simple())
        else:
            left = self.token >> 'IDENTIFIER'
            op = self.operator()
            if self.token >> 'IDENTIFIER':
                right = self.token >> 'IDENTIFIER'
                cond = context.Condition(left, right, op, False)
            else:
                right = self.token >> 'PARAMETER'
                check_name = procedure.parameters.get(right)
                if not check_name:
                    logger.error('Parameter %s not found in procedure parameters', right)
                elif not isinstance(check_name, context.InputParameter):
                    logger.error('The parameter %s must be input', right)
                cond = context.Condition(left, right, op, True)
        return cond

    @log(logger)
    def operator(self):
        # EQ
        # LESS
        # MORE
        # NOT_EQ
        # LESS_OR_EQ
        # MORE_OR_EQ
        op = self.token
        if op not in ('EQ', 'LESS', 'MORE', 'NOT_EQ', 'LESS_OR_EQ', 'MORE_OR_EQ'):
            raise Exception  # todo
        self.token.next()  # self.token >> ...
        return op

    @log(logger)
    def sequence_declaration(self):
        # CREATE SEQUENCE id SEMICOLON
        self.token >> 'SEQUENCE'
        sequence_name = self.token >> 'IDENTIFIER'
        self.token >> 'SEMICOLON'
