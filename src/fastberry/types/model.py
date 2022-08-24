"""
    [API Types] aka [Models]
"""

import dataclasses as dc
import functools
import typing
from collections import OrderedDict

from .scalars import (
    JSON,
    SQLALCHEMY_ACTIVE,
    SQLALCHEMY_BASE,
    STRAWBERRY_CORE,
    STRAWBERRY_FIELDS,
    TEXT,
    AnnotationConfig,
    Manager,
    Scalars,
    TableConfig,
    TypeConfig,
    get_module_name,
)
from .sqlalchemy import create_sqlalchemy_model

CUSTOM_SCALARS = [TEXT, JSON]


class Globals:
    """API Globals"""

    @staticmethod
    def set(key, value):
        """Set"""
        globals().update({key: value})

    @staticmethod
    def get(key):
        """Get"""
        return globals().get(key)


class BaseClass:
    """API Base Class"""

    _id: typing.Optional[str] = None
    id: typing.Optional[STRAWBERRY_FIELDS.ID] = None


def get_field_annotation_core(single_annotation: typing.Any, found_args: tuple):
    """Field Core Annotation"""
    core_arg = None
    has_children = []

    # Core Arg
    if found_args:
        core_arg = found_args[0]
    else:
        core_arg = single_annotation

    # Core Arg Continued . . .
    has_children = typing.get_args(core_arg)
    if len(has_children) > 0:
        core_arg = has_children[0]
        if isinstance(core_arg, str):
            core_arg = typing.ForwardRef(core_arg)
    return core_arg


def get_annotations_args(single_annotation: typing.Any):
    """Get: Annotations-Data"""
    found_args = typing.get_args(single_annotation)
    real_arg = get_field_annotation_core(single_annotation, found_args)
    is_custom_type = isinstance(real_arg, typing.ForwardRef)
    is_optional = type(None) in found_args
    scalar_arg = None
    is_list = False

    if isinstance(real_arg, str):
        is_custom_type = True

    # print(real_arg)
    if real_arg in CUSTOM_SCALARS:
        fake_arg = Scalars.get(real_arg)
        scalar_arg = real_arg
        real_arg = fake_arg.gql
    else:
        scalar_arg = real_arg

    # IS -> List <YES or NO>
    if found_args and len(typing.get_args(found_args[0])) > 0:
        is_list = True

    # IS -> Step 2 ...
    if len(found_args) == 1:
        is_list = True

    # IS -> Step 3 ...
    if is_list:
        core_arg = typing.List[real_arg]
    else:
        core_arg = real_arg

    # Custom Annotations
    return AnnotationConfig(
        original=single_annotation,
        real=real_arg,
        core=core_arg,
        types=Scalars.get(scalar_arg),
        optional=is_optional,
        is_list=is_list,
        is_dict=scalar_arg == JSON,
        is_custom_type=is_custom_type,
    )


def get_function_fields(model: object):
    """Get Object Fields"""
    __fields = [i for i in dir(model) if not i.startswith("__")]
    return {key: getattr(model, key) for key in __fields}


class Model:
    """Strawberry Type (Basic, SQL, Mongo)"""

    sqlalchemy_base = SQLALCHEMY_BASE
    load = staticmethod(Manager.load)
    json = JSON
    text = TEXT

    def __init__(self, sql=None, mongo=None):
        """Create Custon <Type>"""

        if SQLALCHEMY_ACTIVE:
            SQLBase = (sql,)
        else:
            SQLBase = (object,)

        # Create Custon <Type>
        @staticmethod
        def custom_type(
            original_object: object = None,
            *,
            table_name: str = None,
            primary_key: list = None,
            required: list = None,
            index: list = None,
            unique: list = None,
            unique_together: list = None,
            many_to_many: list = None,
            ignore: list = None,
            is_sql: bool = False,
            is_mongo: bool = False,
        ):
            """DECORATOR-OPTIONAL-ARGUMENT"""
            primary_key = primary_key or []
            required = required or []
            index = index or []
            unique = unique or []
            unique_together = unique_together or []
            many_to_many = many_to_many or []
            ignore = ignore or []

            # Starting Wrapper. . .
            if original_object is None:
                return functools.partial(
                    custom_type,
                    table_name=table_name,
                    primary_key=primary_key,
                    required=required,
                    index=index,
                    unique=unique,
                    unique_together=unique_together,
                    many_to_many=many_to_many,
                    ignore=ignore,
                    is_sql=is_sql,
                    is_mongo=is_mongo,
                )

            # Class [ INFO ]
            class_core_annotations = OrderedDict()
            class_related_fields = OrderedDict()
            class_default_values = OrderedDict()
            class_fields_custom_annotations = OrderedDict()

            # Class [ Utils ]
            util_dataclass_fields = OrderedDict()
            util_default_field_is_auto = False

            # Class [ CUSTOM ]
            custom_class = type(
                original_object.__name__,
                (BaseClass,),
                {},
            )
            custom_class.__annotations__ = {
                **BaseClass.__annotations__,
                **original_object.__annotations__,
            }
            custom_dataclass = dc.dataclass(original_object)

            # Create Default Fields
            for field in dc.fields(custom_dataclass):
                if not isinstance(field.default_factory, dc._MISSING_TYPE):
                    default_value = dc.field(default_factory=field.default_factory)
                elif not isinstance(field.default, dc._MISSING_TYPE):
                    default_value = dc.field(default=field.default)
                else:
                    default_value = dc.field(default=None)
                    util_default_field_is_auto = True
                # Register the (Default Value)
                util_dataclass_fields[field.name] = default_value

            # Field & Annotation
            for field_name, annotation in original_object.__annotations__.items():
                current_annotation = get_annotations_args(annotation)
                # Create the (Default Value)
                default_value = util_dataclass_fields[field_name]
                if util_default_field_is_auto and current_annotation.is_dict:
                    default_value = dc.field(default_factory=dict)
                elif util_default_field_is_auto and current_annotation.is_list:
                    default_value = dc.field(default_factory=list)
                # Default Value
                class_default_values[field_name] = default_value
                # Set the (Default Value)
                setattr(custom_class, field_name, default_value)
                custom_class.__annotations__[field_name] = typing.Optional[
                    current_annotation.core
                ]
                # Register the Annotation and Field for Database
                class_fields_custom_annotations[field_name] = current_annotation
                class_core_annotations[field_name] = current_annotation.core
                # IS Relationships
                if current_annotation.is_custom_type:
                    class_related_fields[field_name] = current_annotation.real

            for field_name, field_function in get_function_fields(
                original_object
            ).items():
                if callable(field_function):
                    # Get the (Original Function)
                    func_annotation = field_function.__annotations__.get("return")
                    current_annotation = get_annotations_args(func_annotation)
                    # Register the Annotation and Field for Database
                    class_fields_custom_annotations[field_name] = current_annotation
                    class_core_annotations[field_name] = current_annotation.core
                    # Set the (Custom Function)
                    if STRAWBERRY_CORE:
                        field_function = STRAWBERRY_CORE.field(field_function)
                    setattr(custom_class, field_name, field_function)
                    # IS Relationships
                    if current_annotation.is_custom_type:
                        class_related_fields[field_name] = current_annotation.real

            # Strawberry
            if STRAWBERRY_CORE:
                custom_class = STRAWBERRY_CORE.type(custom_class)
            elif not STRAWBERRY_CORE:
                custom_class = dc.dataclass(custom_class)

            # Info
            info_class_name = original_object.__name__
            info_class_module_path = original_object.__module__
            info_class_module_name = get_module_name(info_class_module_path)

            if not info_class_module_name:
                info_class_module_name = "main"

            # Info Table
            info_class_table_name = (
                f"{info_class_module_name.lower()}_{info_class_name.lower()}"
            )
            info_class_table_uri = (
                f"{info_class_module_name.lower()}.{info_class_name.lower()}"
            )
            if table_name:
                info_class_table_name = table_name

            # Table Config
            table_config = TableConfig(
                required=lambda key: (key in required),
                primary_key=lambda key: (key in primary_key),
                index=lambda key: (key in index),
                unique=lambda key: (key in unique),
                unique_together=unique_together,
                many_to_many=many_to_many,
                ignore=ignore,
            )

            # Type Config
            type_config = TypeConfig(
                custom_class=custom_class,
                name=info_class_name,
                module=info_class_module_name,
                module_path=info_class_module_path,
                table_name=info_class_table_name,
                table_uri=info_class_table_uri,
                core_fields=class_core_annotations,
                related_fields=class_related_fields,
                default_values=class_default_values,
                custom_annotations=class_fields_custom_annotations,
                table_config=table_config,
                sql=is_sql,
                mongo=is_mongo,
            )

            # Attach <Objects>
            custom_class._lazy_object = False
            custom_class._relationships = None
            if is_mongo:
                custom_class.objects = mongo[info_class_table_name]
            elif is_sql:
                sql_obj = create_sqlalchemy_model(SQLBase, type_config)
                custom_class._lazy_object = sql_obj.lazy
                custom_class._relationships = sql_obj._relationships
                if sql_obj.lazy:
                    custom_class.objects = functools.partial(
                        sql_obj.objects, custom_class
                    )
                else:
                    custom_class.objects = sql_obj.objects
            else:
                custom_class.objects = None

            # Attach <Meta>
            custom_class.__meta__ = type_config

            # Register and Return
            Manager.register_model(name=type_config.name, model=type_config)
            return custom_class

        # Self Definitions
        self.type = custom_type
        self.sql = functools.partial(custom_type, is_sql=True)
        self.mongo = functools.partial(custom_type, is_mongo=True)
