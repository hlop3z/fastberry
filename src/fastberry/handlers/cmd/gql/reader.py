def get_names(part):
    """Get Operations Names"""
    return list(map(lambda x: x["name"], part["fields"]))


def get_info(schema):
    """Get GraphQL (Query & Mutations)"""
    app = schema["__schema"]
    return {
        "query": get_names(app["query"]),
        "mutation": get_names(app["mutation"]),
    }
