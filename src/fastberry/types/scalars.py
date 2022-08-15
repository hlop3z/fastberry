"""
    [API Types] - Map DataClass(Fields) to SQL(Fields) and GQL(Types).
"""

import dataclasses
import datetime
import decimal
import types
import typing
from collections import OrderedDict

# SQLAlchemy
try:
    import sqlalchemy
    from sqlalchemy.ext.declarative import declarative_base

    SQLALCHEMY_ACTIVE = True
    SQLALCHEMY_CORE = sqlalchemy
except ImportError:
    SQLALCHEMY_ACTIVE = False
    SQLALCHEMY_CORE = None

# Strawberry
try:
    import strawberry

    STRAWBERRY_ACTIVE = True
    STRAWBERRY_CORE = strawberry
except ImportError:
    STRAWBERRY_ACTIVE = False
    STRAWBERRY_CORE = None


# Custom Typing
TEXT = typing.TypeVar("TEXT", str, None)
JSON = typing.TypeVar("JSON", object, dict, list, None)


@dataclasses.dataclass(frozen=True)
class AnnotationConfig:
    """Annotation Setup"""

    original: typing.Any
    real: typing.Any
    core: typing.Any
    types: typing.Any
    optional: bool = False
    is_list: bool = False
    is_dict: bool = False
    is_custom_type: bool = False


@dataclasses.dataclass
class APIType:
    """API-Field-Type"""

    name: str
    python: typing.Any
    sql: typing.Any
    gql: typing.Any


@dataclasses.dataclass(frozen=True)
class TableConfig:
    """Table Setup"""

    # table_name: str = None
    required: list = None
    primary_key: list = None
    index: list = None
    unique: list = None
    unique_together: list = None
    many_to_many: dict = None
    ignore: list = None
    # is_sql: bool = False
    # is_mongo: bool = False


@dataclasses.dataclass(frozen=True)
class TypeConfig:
    """Type Setup"""

    custom_class: typing.Any
    name: str  # class_name
    module: str  # class_module
    module_path: str
    core_fields: dict
    related_fields: dict
    default_values: dict
    custom_annotations: dict
    table_config: TableConfig
    table_name: str  # for Databases
    table_uri: str  # for GLOBALS
    mongo: bool = False
    sql: bool = False
    is_super_class: bool = True


# SQLAlchemy-BASE
if SQLALCHEMY_ACTIVE:
    SQLALCHEMY_BASE = declarative_base()
else:
    SQLALCHEMY_BASE = object


class Singleton:
    """Create a Singleton"""

    def __new__(cls, *args, **kwargs):
        """Real INIT"""
        it_id = "__it__"
        it = cls.__dict__.get(it_id, None)
        if it is not None:
            return it
        it = object.__new__(cls)
        setattr(cls, it_id, it)
        it.init(*args, **kwargs)
        return it

    def init(self, *args, **kwargs):
        """Class __init__ Replacement"""


# SQL Relationships
class Globals:
    """API Globals"""

    @staticmethod
    def set(key, value):
        """set"""
        globals().update({key: value})

    @staticmethod
    def get(key):
        """get"""
        return globals().get(key)


class SQLManager(Singleton):
    """SQL Manager"""

    def init(self, *args, **kwargs):
        """Class __init__ Replacement"""
        self.active = SQLALCHEMY_ACTIVE
        self.base = SQLALCHEMY_BASE
        self.models = OrderedDict()
        self.globals = Globals

    def register_model(self, name: str, model: TypeConfig):
        """Register Model"""
        if name in self.models.keys():
            raise Exception(
                f"Duplicate Type: {name}\nExisting Model: {model.module_path}"
            )
        self.models[name] = model
        self.globals.set(name, model.custom_class)

    def find_model(self, name: str):
        """Find Model"""
        return self.globals.get(name)

    @staticmethod
    def load(*models):
        """Load"""
        for model in models:
            if model._lazy_object:
                model.objects()


def sql_easy_relationship(
    model_name: str = None,
    table_name: str = None,
    nullable: bool = True,
    unique: bool = False,
    index: bool = False,
):
    """Create a relationship in SQLAlchemy"""

    if SQLALCHEMY_ACTIVE:
        return sqlalchemy.Column(
            f"""{model_name}_id""",
            sqlalchemy.Integer,
            sqlalchemy.ForeignKey(f"""{table_name}._id"""),
            nullable=nullable,
            unique=unique,
            index=index,
        )
    return None


def sql_many_to_many(
    sql_base: typing.Any = None,
    table_left: str = None,
    table_right: str = None,
):
    """Create a Many-To-Many relationship in SQLAlchemy"""

    if SQLALCHEMY_ACTIVE:
        return sqlalchemy.Table(
            f"""association_{table_left}_and_{table_right}""",
            sql_base.metadata,
            sqlalchemy.Column(
                "left_id",
                sqlalchemy.String(length=255),
                primary_key=True,
            ),
            sqlalchemy.Column(
                "right_id",
                sqlalchemy.String(length=255),
                primary_key=True,
            ),
            sqlalchemy.UniqueConstraint("left_id", "right_id"),
        )
    return None


# CORE Fields
ALL_FIELDS = [
    "String",
    "Text",
    "Integer",
    "Float",
    "Boolean",
    "Date",
    "DateTime",
    "Time",
    "Decimal",
    "JSON",
    "ForeignKey",
    "UniqueTogether",
]

# Init Fields
SQLALCHEMY_FIELDS = types.SimpleNamespace(**{key: key for key in ALL_FIELDS})
STRAWBERRY_FIELDS = types.SimpleNamespace(**{key: key for key in ["ID", "JSON"]})

SQLALCHEMY_COLUMN = None
SQLALCHEMY_UNIQUE = None

STRAWBERRY_FIELDS.ID = str
STRAWBERRY_FIELDS.JSON = dict

# Map SQL
if SQLALCHEMY_ACTIVE:
    # Core
    SQLALCHEMY_FIELDS.Base = SQLALCHEMY_BASE
    SQLALCHEMY_FIELDS.Table = sqlalchemy.Table
    SQLALCHEMY_FIELDS.Column = sqlalchemy.Column
    SQLALCHEMY_FIELDS.ForeignKey = sqlalchemy.ForeignKey
    SQLALCHEMY_FIELDS.UniqueTogether = sqlalchemy.UniqueConstraint
    # Fields
    SQLALCHEMY_FIELDS.String = sqlalchemy.String(length=255)
    SQLALCHEMY_FIELDS.Text = sqlalchemy.Text
    SQLALCHEMY_FIELDS.Integer = sqlalchemy.Integer
    SQLALCHEMY_FIELDS.Float = sqlalchemy.Float
    SQLALCHEMY_FIELDS.Boolean = sqlalchemy.Boolean
    SQLALCHEMY_FIELDS.Date = sqlalchemy.Date
    SQLALCHEMY_FIELDS.DateTime = sqlalchemy.DateTime
    SQLALCHEMY_FIELDS.Time = sqlalchemy.Time
    SQLALCHEMY_FIELDS.Decimal = sqlalchemy.DECIMAL
    SQLALCHEMY_FIELDS.JSON = sqlalchemy.JSON


# Map GQL
if STRAWBERRY_ACTIVE:
    STRAWBERRY_FIELDS.ID = strawberry.ID
    STRAWBERRY_FIELDS.JSON = strawberry.scalars.JSON

# Core Init
CORE = {}

# Core Values
CORE[TEXT] = APIType(
    name="Text",
    python=TEXT,
    sql=SQLALCHEMY_FIELDS.Text,
    gql=str,
)

CORE[JSON] = APIType(
    name="JSON",
    python=JSON,
    sql=SQLALCHEMY_FIELDS.JSON,
    gql=STRAWBERRY_FIELDS.JSON,
)

CORE[str] = APIType(
    name="String",
    python=str,
    sql=SQLALCHEMY_FIELDS.String,
    gql=str,
)

CORE[int] = APIType(
    name="Integer",
    python=int,
    sql=SQLALCHEMY_FIELDS.Integer,
    gql=int,
)

CORE[float] = APIType(
    name="Float",
    python=float,
    sql=SQLALCHEMY_FIELDS.Float,
    gql=float,
)

CORE[bool] = APIType(
    name="Boolean",
    python=bool,
    sql=SQLALCHEMY_FIELDS.Boolean,
    gql=bool,
)

CORE[datetime.date] = APIType(
    name="Date",
    python=datetime.date,
    sql=SQLALCHEMY_FIELDS.Date,
    gql=datetime.date,
)

CORE[datetime.datetime] = APIType(
    name="DateTime",
    python=datetime.datetime,
    sql=SQLALCHEMY_FIELDS.DateTime,
    gql=datetime.datetime,
)

CORE[datetime.time] = APIType(
    name="Time",
    python=datetime.time,
    sql=SQLALCHEMY_FIELDS.Time,
    gql=datetime.time,
)

CORE[decimal.Decimal] = APIType(
    name="Decimal",
    python=decimal.Decimal,
    sql=SQLALCHEMY_FIELDS.Decimal,
    gql=decimal.Decimal,
)

CORE_ID = APIType(
    name="ID",
    python=str,
    sql=str,
    gql=STRAWBERRY_FIELDS.ID,
)


def get_module_name(name: str):
    """Get: Class-Module's Name"""
    parts = name.split(".")
    if parts[0] == "apps" and len(parts) > 1:
        parts.pop(0)
    module_name = parts[0]
    if module_name == "__main__":
        module_name = None
    return module_name


# SCALARS
Scalars = CORE.copy()

# MANAGER
Manager = SQLManager()
