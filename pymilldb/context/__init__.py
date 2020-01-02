from .Column import Column
from .Condition import Condition
from .DataType import Int, Float, Double, Char, get_type_by_name
from .Procedure import Procedure
from .Table import Table
from .Parameter import InputParameter, OutputParameter
from .Statement import SelectStatement, InsertStatement
from .Selection import Selection

NAME = ""

TABLES = {}
PROCEDURES = {}
SEQUENCES = {}

VARIABLES = {}
