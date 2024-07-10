from sqlalchemy.types import UserDefinedType
from sqlalchemy.ext.compiler import compiles
import numpy as np
from sqlalchemy.dialects import postgresql

class Vector(UserDefinedType):
    def __init__(self, dimensions=1536):
        self.dimensions = dimensions

    def get_col_spec(self):
        return f"vector({self.dimensions})"

    def bind_processor(self, dialect):
        def process(value):
            return list(value) if value is not None else None
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return np.array(value) if value is not None else None
        return process

    def compare_against_backend(self, dialect, conn_type):
        return isinstance(conn_type, postgresql.ARRAY)

@compiles(Vector, "postgresql")
def compile_vector(element, compiler, **kw):
    return f"vector({element.dimensions})"

# Register the custom type with SQLAlchemy
from sqlalchemy.dialects.postgresql.base import ischema_names
ischema_names['vector'] = Vector