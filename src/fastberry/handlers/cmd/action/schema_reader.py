"""
    Read & Transform the GraphQL Schema.
"""

import typing

SCALAR_TYPES = [
    "ID",
    "String",
    "Int",  # Integer
    "Float",
    "Boolean",
    "Decimal",
    "Date",
    "Datetime",
    "Time",
    "JSON",
]


class TypeModel(typing.TypedDict):
    """Object Info"""

    type: str
    name: str
    scalar: bool
    list: bool
    required: bool
    default: typing.Any


def set_default_value(setup):
    """Fix Default Value"""
    python_scalar = [
        "ID",
        "String",
        "Int",  # Integer
        "Float",
        "Boolean",
        "Decimal",
        "Date",
        "Datetime",
        "Time",
    ]
    if setup["default"] == "null":
        setup["default"] = None
    elif setup["scalar"] and setup["type"] in python_scalar:
        match setup["type"]:
            case "String":
                setup["default"] = str(setup["default"])
            case "Int":
                setup["default"] = int(setup["default"])
            case "Float":
                setup["default"] = float(setup["default"])
            case "Boolean":
                setup["default"] = setup["default"] == "true"
            case _:
                setup["default"] = str(setup["default"])
    return setup


def get_real_type(field):
    """Get Type from GraphQL Schema { Introspection }"""
    type_kind = field["type"]["kind"]
    type_name = field["type"]["name"]
    setup = None
    default_value = field.get("defaultValue") or "null"
    match type_kind:
        case "SCALAR":
            setup = TypeModel(
                type=field["type"]["name"],
                name=field.get("name"),
                scalar=True,
                list=False,
                required=False,
                default=default_value,
            )
        case "OBJECT":
            setup = TypeModel(
                type=type_name,
                name=field.get("name"),
                scalar=False,
                list=False,
                required=False,
                default=default_value,
            )
        case "LIST":
            child_type = field["type"]["ofType"]["ofType"]
            setup = TypeModel(
                type=child_type.get("name"),
                name=field.get("name"),
                scalar=child_type["kind"] == "SCALAR",
                list=True,
                required=False,
                default=default_value,
            )
        case "UNION":
            setup = TypeModel(
                type=type_name,
                name=field.get("name"),
                scalar=False,
                list=False,
                required=False,
                default=default_value,
            )
        case "NON_NULL":
            child_type = field["type"]["ofType"]
            match child_type["kind"]:
                case "SCALAR":
                    setup = TypeModel(
                        type=child_type.get("name"),
                        name=field.get("name"),
                        scalar=True,
                        list=False,
                        required=True,
                        default=default_value,
                    )
                case "OBJECT":
                    setup = TypeModel(
                        type=child_type.get("name"),
                        name=field.get("name"),
                        scalar=False,
                        list=False,
                        required=True,
                        default=default_value,
                    )
                case "LIST":
                    child_type = child_type["ofType"]
                    setup = TypeModel(
                        type=child_type.get("name"),
                        name=field.get("name"),
                        scalar=child_type["kind"] == "SCALAR",
                        list=True,
                        required=True,
                        default=default_value,
                    )
                case "UNION":
                    setup = TypeModel(
                        type=child_type.get("name"),
                        name=field.get("name"),
                        scalar=False,
                        list=False,
                        required=True,
                        default=default_value,
                    )
    setup = set_default_value(setup)
    return setup


def create_types(graphql_info):
    """Get Types from GraphQL Schema { Introspection }"""
    the_type = {}
    for active in graphql_info:
        the_fields = []
        for field in active["fields"]:
            the_fields.append(get_real_type(field))
        the_type[active["name"]] = the_fields
    return the_type


def create_inputs(graphql_info):
    """Get Inputs from GraphQL Schema { Introspection }"""
    the_type = {}
    for active in graphql_info:
        the_fields = []
        for field in active["fields"]:
            default_value = field.get("defaultValue") or "null"
            match field["type"]["kind"]:
                case "SCALAR":
                    setup = TypeModel(
                        type=field["type"]["name"],
                        name=field.get("name"),
                        scalar=True,
                        list=False,
                        required=False,
                        default=default_value,
                    )
                case "INPUT_OBJECT":
                    child_type = field["type"]
                    setup = TypeModel(
                        type=child_type.get("name"),
                        name=field.get("name"),
                        scalar=False,
                        list=False,
                        required=False,
                        default=default_value,
                    )
                case "LIST":
                    child_type = field["type"]["ofType"]
                    if child_type["kind"] == "NON_NULL":
                        child_type = child_type["ofType"]
                    setup = TypeModel(
                        type=child_type.get("name"),
                        name=field.get("name"),
                        scalar=child_type["kind"] == "SCALAR",
                        list=True,
                        required=True,
                        default=default_value,
                    )
                case "NON_NULL":
                    child_type = field["type"]["ofType"]
                    match child_type["kind"]:
                        case "INPUT_OBJECT":
                            setup = TypeModel(
                                type=child_type.get("name"),
                                name=field.get("name"),
                                scalar=False,
                                list=False,
                                required=True,
                                default=default_value,
                            )
                        case "LIST":
                            child_type = child_type["ofType"]
                            if child_type["kind"] == "NON_NULL":
                                child_type = child_type["ofType"]
                            setup = TypeModel(
                                type=child_type.get("name"),
                                name=field.get("name"),
                                scalar=child_type["kind"] == "SCALAR",
                                list=True,
                                required=True,
                                default=default_value,
                            )
                        case "SCALAR":
                            setup = TypeModel(
                                type=child_type.get("name"),
                                name=field.get("name"),
                                scalar=True,
                                list=False,
                                required=True,
                                default=default_value,
                            )
            setup = set_default_value(setup)
            the_fields.append(setup)
        the_type[active["name"]] = the_fields
    return the_type


def get_return_types(graphql_info):
    """API Return-Types"""
    responses = {}
    for item in graphql_info:
        real_type = item["response"]
        real_type = get_real_type({"type": real_type})
        # if real_type["type"].endswith("Connection"):
        #    real_type["type"] = real_type["type"].replace("Connection", "")
        del real_type["name"]
        del real_type["default"]
        responses[item["name"]] = real_type
    return responses


def get_info(schema):
    """Get Schema Info { Introspection }"""
    graphql_info = {
        "forms": [],
        "types": [],
        "ops": {
            "query": [],
            "mutation": [],
        },
        "returnTypes": {
            "query": [],
            "mutation": [],
        },
    }
    for item in schema["__schema"]["types"]:
        kind = item["kind"]
        match kind:
            case "INPUT_OBJECT":
                graphql_info["forms"].append(
                    {"name": item["name"], "fields": item["inputFields"]}
                )
            case "OBJECT":
                if item["name"] not in ["Query", "Mutation"] and not item[
                    "name"
                ].startswith("__"):
                    graphql_info["types"].append(
                        {"name": item["name"], "fields": item["fields"]}
                    )
                elif item["name"] in ["Query", "Mutation"]:
                    match item["name"]:
                        case "Query":
                            graphql_info["ops"]["query"] = [
                                {
                                    "name": active["name"],
                                    "fields": active["args"],
                                    "response": active["type"],
                                }
                                for active in item["fields"]
                            ]
                        case "Mutation":
                            graphql_info["ops"]["mutation"] = [
                                {
                                    "name": active["name"],
                                    "fields": active["args"],
                                    "response": active["type"],
                                }
                                for active in item["fields"]
                            ]

    # Custom Typing
    graphql_info["returnTypes"]["query"] = get_return_types(
        graphql_info["ops"]["query"]
    )
    graphql_info["returnTypes"]["mutation"] = get_return_types(
        graphql_info["ops"]["mutation"]
    )
    graphql_info["types"] = create_types(graphql_info["types"])
    graphql_info["forms"] = create_types(graphql_info["forms"])
    graphql_info["ops"]["query"] = create_inputs(graphql_info["ops"]["query"])
    graphql_info["ops"]["mutation"] = create_inputs(graphql_info["ops"]["mutation"])
    return graphql_info


# Introspection Query
INTROSPECTION_QUERY = """
query IntrospectionQuery {
	__schema {
		types {
			...FullType
		}
	}
}

fragment FullType on __Type {
	kind
	name
	fields(includeDeprecated: true) {
		name
		args {
			...InputValue
		}
		type {
			...TypeRef
		}
	}
	inputFields {
		...InputValue
	}
	interfaces {
		...TypeRef
	}
	enumValues(includeDeprecated: true) {
		name
		isDeprecated
		deprecationReason
	}
	possibleTypes {
		...TypeRef
	}
}

fragment InputValue on __InputValue {
	name
	type {
		...TypeRef
	}
	defaultValue
}

fragment TypeRef on __Type {
	kind
	name
	ofType {
		kind
		name
		ofType {
			kind
			name
			ofType {
				kind
				name
				ofType {
					kind
					name
					ofType {
						kind
						name
						ofType {
							kind
							name
							ofType {
								kind
								name
							}
						}
					}
				}
			}
		}
	}
}
"""
