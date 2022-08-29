DB_URL = {
    "SQL": "sqlite:///examples.db",
    "MONGO": "mongodb://localhost:27017/examples",
}

DATABASES = {
    "mongo": {
        "default": DB_URL["MONGO"],
        #"another-database": DB_URL["MONGO"],
    },
    "sql": {
        "default": DB_URL["SQL"],
        # "another-database": DB_URL["SQL"],
    },
}
