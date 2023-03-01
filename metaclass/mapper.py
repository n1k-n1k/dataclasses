from sqlalchemy.orm import registry
from sqlalchemy.schema import MetaData

metadata = MetaData(schema='sch')
dataclass_mapper = registry(metadata=metadata)
