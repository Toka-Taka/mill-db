def program(lex):
    # <program_element_list>
    pass


def program_element_list(lex):
    # <program_element>
    # <program_element_list> <program_element>
    pass


def program_element(lex):
    # <table_declaration>
    # <procedure_declaration>
    # <sequence_declaration>
    pass


def table_declaration(lex):
    # CREATE TABLE id LPARENT <column_declaration_list> RPARENT SEMICOLON
    pass


def column_declaration_list(lex):
    # id type
    # id type PK
    pass


def procedure_declaration(lex):
    # CREATE PROCEDURE id LPARENT <parameter_declaration_list> RPARENT BEGIN <statement_list> END SEMICOLON
    pass


def parameter_declaration_list(lex):
    # <parameter_declaration>
    # <parameter_declaration_list> COMMA <parameter_declaration>
    pass


def parameter_declaration(lex):
    # pid type <parameter_mode>
    pass


def parameter_mode(lex):
    # IN
    # OUT
    pass


def statement_list(lex):
    # <statement>
    # <statement_list> <statement>
    pass


def statement(lex):
    # <insert_statement>
    # <select_statement>
    pass


def insert_statement(lex):
    # INSERT TABLE id VALUES LPARENT <argument_list> RPARENT SEMICOLON
    pass


def argument_list(lex):
    # <argument>
    # <argument_list> COMMA <argument>
    pass


def argument(lex):
    # pid
    # CURRVAL LPARENT id RPARENT
    # NEXTVAL LPARENT id RPARENT
    pass


def select_statement(lex):
    # SELECT <selection_list> FROM <table_list> WHERE <condition_list> SEMICOLON
    pass


def selection_list(lex):
    # <selection>
    # <selection_list> COMMA <selection>
    pass


def selection(lex):
    # id SET pid
    pass


def table_list(lex):
    # <table_list> JOIN id
    # id
    pass


def condition_list(lex):
    # <search_cond_not>
    # <search_cond_not> AND <condition_list>
    # <search_cond_not> OR <condition_list>
    # LPARENT <condition_list> RPARENT
    # LPARENT <condition_list> RPARENT AND <condition_list>
    # LPARENT <condition_list> RPARENT OR <condition_list>
    pass


def search_cond_not(lex):
    # <condition_simple>
    # NOT <condition_simple>
    pass


def condition_simple(lex):
    # id <operator> pid
    # id <operator> id
    pass


def operator(lex):
    # EQ
    # LESS
    # MORE
    # NOT_EQ
    # LESS_OR_EQ
    # MORE_OR_EQ
    pass


def sequence_declaration(lex):
    # CREATE SEQUENCE id SEMICOLON
    pass
