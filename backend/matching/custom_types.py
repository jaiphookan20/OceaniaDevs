from sqlalchemy.types import UserDefinedType
from sqlalchemy.ext.compiler import compiles
import numpy as np

class Vector(UserDefinedType):
    def __init__(self, dimensions=1536):
        self.dimensions = dimensions

    def get_col_spec(self):
        return f"VECTOR({self.dimensions})"

    def bind_processor(self, dialect):
        def process(value):
            return list(value) if value is not None else None
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return np.array(value) if value is not None else None
        return process

@compiles(Vector, "postgresql")
def compile_vector(element, compiler, **kw):
    return f"VECTOR({element.dimensions})"


