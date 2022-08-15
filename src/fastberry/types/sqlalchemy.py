"""
SQL-Alchemy ORM to Custom-Types Mapper
"""
import functools
import types
import typing

from .scalars import SQLALCHEMY_ACTIVE, SQLALCHEMY_FIELDS, Manager, sql_many_to_many


def related_field(type_config, key, related_class_name):
    """
    Get Related Fields
    """
    # is_many_to_many = table_config.many_to_many.get(key)
    table_config = type_config.table_config
    related_model = Manager.find_model(related_class_name)
    related_table = related_model.__meta__.table_name
    if not related_model.__meta__.sql:
        # Mongo Database
        return SQLALCHEMY_FIELDS.Column(
            SQLALCHEMY_FIELDS.String,
            index=table_config.index(key),
            unique=table_config.unique(key),
            primary_key=table_config.primary_key(key),
            nullable=not table_config.required(key),
        )
    # SQL Database
    return SQLALCHEMY_FIELDS.Column(
        SQLALCHEMY_FIELDS.Integer,
        SQLALCHEMY_FIELDS.ForeignKey(f"{related_table}._id"),
        index=table_config.index(key),
        unique=table_config.unique(key),
        primary_key=table_config.primary_key(key),
        nullable=not table_config.required(key),
    )


# sqlalchemy_base
def related_many_to_many(sqlalchemy_base, type_config, related_class_name):
    """
    Get Related Many-To-Many Fields
    """
    # is_many_to_many = table_config.many_to_many.get(key)
    related_model = Manager.find_model(related_class_name)
    related_table = related_model.__meta__.table_name
    return sql_many_to_many(sqlalchemy_base, type_config.table_name, related_table)


def create_sqlalchemy_model(base, type_config):
    """
    Create SQLAlchemy Model
    """
    if SQLALCHEMY_ACTIVE:
        sqlalchemy_base = base
        sqlalchemy_class_name = f"{type_config.name}SQLAlchemy"
        table_config = type_config.table_config
        # Table Setup
        sqlalchemy_class_setup = {
            "__tablename__": type_config.table_name,
            "__table_args__": [],
            "_id": SQLALCHEMY_FIELDS.Column(
                SQLALCHEMY_FIELDS.Integer, primary_key=True
            ),
        }
        sqlalchemy_setup_lazy_load = {}
        sqlalchemy_many_to_many_lazy_load = {}
        sqlalchemy_many_to_many = {}
        one_or_more_sqlalchemy_lazy_load = False
        # Get Fields
        for key, setup in type_config.custom_annotations.items():
            if not setup.is_list and not key in table_config.ignore:
                sqlalchemy_lazy_load = False
                if not setup.types:
                    column_name = f"{key}_id"
                    if isinstance(setup.real, typing.ForwardRef):
                        related_class_name = setup.real.__forward_arg__
                    elif isinstance(setup.real, str):
                        related_class_name = setup.real
                    related_model = Manager.find_model(related_class_name)
                    if not related_model:
                        sqlalchemy_lazy_load = True
                        one_or_more_sqlalchemy_lazy_load = True
                    # Many-To-Many Relationship or Regular Relationship?
                    if not key in table_config.many_to_many:
                        # Lazy Load or Load Now?
                        if sqlalchemy_lazy_load:
                            sqlalchemy_setup_lazy_load[column_name] = functools.partial(
                                related_field, type_config, key, related_class_name
                            )
                        else:
                            sqlalchemy_class_setup[column_name] = related_field(
                                type_config, key, related_class_name
                            )
                    else:
                        if sqlalchemy_lazy_load:
                            do_many_to_many = functools.partial(
                                related_many_to_many,
                                sqlalchemy_base[0],
                                type_config,
                                related_class_name,
                            )
                            sqlalchemy_many_to_many_lazy_load[key] = do_many_to_many
                        else:
                            do_many_to_many = related_many_to_many(
                                sqlalchemy_base[0],
                                type_config,
                                related_class_name,
                            )
                            sqlalchemy_many_to_many[key] = do_many_to_many

                else:
                    sqlalchemy_class_setup[key] = SQLALCHEMY_FIELDS.Column(
                        setup.types.sql,
                        index=table_config.index(key),
                        unique=table_config.unique(key),
                        primary_key=table_config.primary_key(key),
                        nullable=not table_config.required(key),
                    )

        for config in table_config.unique_together:
            unique_together = SQLALCHEMY_FIELDS.UniqueTogether(*config)
            sqlalchemy_class_setup["__table_args__"].append(unique_together)

        sqlalchemy_class_setup["__table_args__"] = tuple(
            sqlalchemy_class_setup["__table_args__"]
        )

        class LoadLater:
            """Load Objects (aka: SQLAlchemy ORM)"""

            def __init__(self):
                """Init Load-Later"""
                self.lazy = True
                self.objects = None
                self._relationships = None

                if not one_or_more_sqlalchemy_lazy_load:
                    self.lazy = False
                    # Objects
                    self.objects = type(
                        sqlalchemy_class_name, sqlalchemy_base, sqlalchemy_class_setup
                    ).__table__
                    # Relationship
                    self._relationships = types.SimpleNamespace(
                        **sqlalchemy_many_to_many
                    )
                else:
                    relationship_setup = sqlalchemy_many_to_many

                    def load_table(cls):
                        """When Ready Load Tables"""
                        for key, lazy_load in sqlalchemy_setup_lazy_load.items():
                            if callable(lazy_load):
                                sqlalchemy_class_setup[key] = lazy_load()
                            else:
                                sqlalchemy_class_setup[key] = lazy_load

                        # Objects
                        cls.objects = type(
                            sqlalchemy_class_name,
                            sqlalchemy_base,
                            sqlalchemy_class_setup,
                        ).__table__
                        for key, lazy_load in sqlalchemy_many_to_many_lazy_load.items():
                            if callable(lazy_load):
                                relationship_setup[key] = lazy_load()
                            else:
                                relationship_setup[key] = lazy_load
                        for key, loader in sqlalchemy_many_to_many.items():
                            relationship_setup[key] = loader

                        # Relationship
                        cls._relationships = types.SimpleNamespace(**relationship_setup)

                    # Objects
                    self.objects = load_table

        return LoadLater()
    return None
