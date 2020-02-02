from .Argument import ArgumentParameter, ArgumentSequenceCurrent, ArgumentSequenceNext
from .Column import Column
from .Condition import Condition
from .DataType import Int, Float, Double, Char, get_type_by_name
from .Parameter import InputParameter, OutputParameter
from .Procedure import Procedure, logger as procedure_logger
from .Selection import Selection
from .Sequence import Sequence
from .Statement import SelectStatement, InsertStatement, logger as statement_logger
from .Table import Table

NAME = ""

TABLES = {}
PROCEDURES = {}
SEQUENCES = {}

VARIABLES = {}
