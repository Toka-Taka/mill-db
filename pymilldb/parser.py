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
        # <program_element>+
        self.program_element()
        while self.token != 'END_CHAR':
            self.program_element()

    @log(logger)
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
        else:
            raise Exception  # todo

    @log(logger)
    def table_declaration(self):
        # CREATE TABLE id LPARENT <column_declaration_list> RPARENT SEMICOLON
        self.token.next()  # self.token >> 'TABLE'
        table_name = self.token >> 'IDENTIFIER'
        table = context.Table(table_name)
        check_name = context.VARIABLES.get(table_name)
        if check_name:
            logger.error('Table name `%s` is already used for the %s.', table_name, check_name)
        else:
            context.VARIABLES[table_name] = 'table'
            context.TABLES[table_name] = table
        self.token >> 'LPARENT'
        self.column_declaration_list(table)
        self.token >> 'RPARENT'
        self.token.safe() >> 'SEMICOLON'

    @log(logger)
    def column_declaration_list(self, table: context.Table):
        # column_declaration_list (COMMA column_declaration)*
        self.column_declaration(table)
        while self.token == 'COMMA':
            self.token.next()  # self.token >> 'COMMA'
            self.column_declaration(table)

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
        column = context.Column(column_name, column_type, is_pk, table)
        table.add_column(column)

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
        procedure = context.Procedure(procedure_name)
        if check_name:
            logger.error('Procedure name `%s` is already used for the %s.', procedure_name, check_name)
        else:
            context.VARIABLES[procedure_name] = 'procedure'
            context.PROCEDURES[procedure_name] = procedure
        self.token >> 'LPARENT'
        self.parameter_declaration_list(procedure)
        self.token >> 'RPARENT'
        self.token.safe() >> 'BEGIN'
        self.statement_list(procedure)
        self.token.safe() >> 'END'
        self.token.safe() >> 'SEMICOLON'

    @log(logger)
    def parameter_declaration_list(self, procedure: context.Procedure):
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
        else:
            logger.fatal('Not found parameter type (`in` or `out`)')
            raise Exception
        procedure.add_parameter(parameter)

    @log(logger)
    def statement_list(self, procedure: context.Procedure):
        # <statement>+
        self.statement(procedure)
        while self.token == 'INSERT' or self.token == 'SELECT':
            self.statement(procedure)

    @log(logger)
    def statement(self, procedure: context.Procedure):
        # <insert_statement>
        # <select_statement>
        if self.token == 'INSERT':
            if procedure.mode is None:
                procedure.set_mode_to_write()
            self.insert_statement(procedure)
        elif self.token == 'SELECT':
            if procedure.mode is None:
                procedure.set_mode_to_read()
            self.select_statement(procedure)
        else:
            logger.fatal('Unreachable exception')
            raise Exception  # todo

    @log(logger)
    def insert_statement(self, procedure: context.Procedure):
        # INSERT TABLE id VALUES LPARENT <argument_list> RPARENT SEMICOLON
        self.token.next()  # self.token >> 'INSERT'
        self.token >> 'TABLE'
        table_name = self.token >> 'IDENTIFIER'
        table = context.TABLES.get(table_name)
        # Check exists table
        if not table:
            context.statement_logger.error('Table %s not found', table_name)
        insert_statement = context.InsertStatement(procedure, table)
        self.token >> 'VALUES'
        self.token >> 'LPARENT'
        self.argument_list(procedure, insert_statement)
        # Check num columns and num arguments
        if table and len(table.columns) != len(insert_statement.arguments):
            context.statement_logger.error('Incorrect number of arguments')
        self.token >> 'RPARENT'
        self.token >> 'SEMICOLON'
        procedure.add_statement(insert_statement)

    @log(logger)
    def argument_list(self, procedure: context.Procedure, insert_statement: context.InsertStatement):
        # <argument> (COMMA <argument>)*
        self.argument(procedure, insert_statement)
        while self.token == 'COMMA':
            self.token.next()  # self.token >> 'COMMA'
            self.argument(procedure, insert_statement)

    @log(logger)
    def argument(self, procedure: context.Procedure, insert_statement: context.InsertStatement):
        # pid
        # CURRVAL LPARENT id RPARENT
        # NEXTVAL LPARENT id RPARENT
        if self.token == 'CURRVAL':
            self.token.next()  # self.token >> 'CURRVAL'
            self.token >> 'LPARENT'
            sequence_name = self.token >> 'IDENTIFIER'
            sequence = context.SEQUENCES.get(sequence_name)
            if not sequence:
                context.statement_logger.error('Sequence %s not found', sequence_name)
            argument = context.ArgumentSequenceCurrent(sequence_name, sequence)
            self.token >> 'RPARENT'
            insert_statement.arguments.append(argument)

        elif self.token == 'NEXTVAL':
            self.token.next()  # self.token >> 'NEXTVAL'
            self.token >> 'LPARENT'
            sequence_name = self.token >> 'IDENTIFIER'
            sequence = context.SEQUENCES.get(sequence_name)
            if not sequence:
                context.statement_logger.error('Sequence %s not found', sequence_name)
            argument = context.ArgumentSequenceNext(sequence_name, sequence)
            self.token >> 'RPARENT'
            insert_statement.arguments.append(argument)

        elif self.token == 'PARAMETER':
            parameter_name = self.token >> 'PARAMETER'
            parameter = procedure.parameters.get(parameter_name)
            if not parameter:
                context.statement_logger.error('Parameter %s not found in procedure parameters', parameter_name)
            elif not isinstance(parameter, context.InputParameter):
                context.statement_logger.error('The parameter %s must be input', parameter_name)
            argument = context.ArgumentParameter(parameter_name, parameter)
            insert_statement.arguments.append(argument)

        else:
            logger.error('Expected `currval` or `nextval` or <parameter>')

    @log(logger)
    def select_statement(self, procedure: context.Procedure):
        # SELECT <selection_list> FROM <table_list> WHERE <condition_list> SEMICOLON
        self.token.next()  # self.token >> 'SELECT'
        select_statement = context.SelectStatement(procedure)
        self.selection_list(procedure, select_statement)
        self.token >> 'FROM'
        self.table_list(select_statement)
        select_statement.check_selections()
        self.token >> 'WHERE'
        conditions = self.condition_list(procedure, select_statement)
        self.token.safe() >> 'SEMICOLON'
        procedure.add_statement(select_statement)

    @log(logger)
    def selection_list(self, procedure: context.Procedure, select_statement: context.SelectStatement):
        # <selection> (COMMA <selection>)*
        self.selection(procedure, select_statement)
        while self.token == 'COMMA':
            self.token.next()  # self.token >> 'COMMA'
            self.selection(procedure, select_statement)

    @log(logger)
    def selection(self, procedure: context.Procedure, select_statement: context.SelectStatement):
        # id SET pid
        column_name = self.token >> 'IDENTIFIER'
        self.token >> 'SET'
        parameter_name = self.token >> 'PARAMETER'
        parameter = procedure.parameters.get(parameter_name)
        if not parameter:
            context.statement_logger.error('Parameter %s not found in procedure parameters', parameter_name)
        elif not isinstance(parameter, context.OutputParameter):
            context.statement_logger.error('The parameter %s must be output', parameter_name)
        select_statement.raw_selections.append((column_name, parameter))

    @log(logger)
    def table_list(self, select_statement: context.SelectStatement):
        # id (JOIN id)*
        table_name = self.token >> 'IDENTIFIER'
        table = context.TABLES.get(table_name)
        if not table:
            context.statement_logger.error('Table %s not found', table_name)
        else:
            select_statement.add_table(table)

        while self.token == 'JOIN':
            self.token.next()  # self.token >> 'JOIN'
            table_name = self.token >> 'IDENTIFIER'
            table = context.TABLES.get(table_name)
            if not table:
                context.statement_logger.error('Table %s not found', table_name)
            else:
                select_statement.add_table(table)

    @log(logger)
    def condition_list(self, procedure: context.Procedure, select_statement: context.Statement):
        # <condition_simple> (OR|AND <condition_simple>)*
        cond = self.condition_simple(procedure, select_statement)
        interim_out = [[cond]]
        while True:
            if self.token == 'AND':
                self.token.next()  # self.token >> 'AND'
                interim_out[-1].append(self.condition_simple(procedure, select_statement))
            elif self.token == 'OR':
                self.token.next()  # self.token >> 'OR'
                interim_out.append([self.condition_simple(procedure, select_statement)])
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
    def condition_simple(self, procedure: context.Procedure, select_statement: context.Statement):
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
            if self.token == 'IDENTIFIER':
                right = self.token >> 'IDENTIFIER'
                cond = context.Condition(left, right, op, False)
            elif self.token == 'PARAMETER':
                right = self.token >> 'PARAMETER'
                check_name = procedure.parameters.get(right)
                if not check_name:
                    logger.error('Parameter %s not found in procedure parameters', right)
                elif not isinstance(check_name, context.InputParameter):
                    logger.error('The parameter %s must be input', right)
                cond = context.Condition(left, right, op, True)
            else:
                raise Exception  # todo
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
        sequence = context.Sequence(sequence_name)
        check_name = context.VARIABLES.get(sequence_name)
        if check_name:
            logger.error('Sequence name `%s` is already used for the %s', sequence_name, check_name)
        else:
            context.SEQUENCES[sequence_name] = sequence
            context.VARIABLES[sequence_name] = 'sequence'
        self.token >> 'SEMICOLON'
