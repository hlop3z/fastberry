# Operations **Layout**

```text
MY_APP/                 --> <Directory> - Your App Directory.
|
|--  operations/        --> <Directory> - Your GraphQL's Operations in HERE.
|    |-- core/          --> <File> - Use in both (Desktop & Mobile).
|    |-- desktop/       --> <File> - Use in Desktop.
|    `-- mobile/        --> <File> - Use in Mobile.
|
`-- etc...
```

Create your own **Files** inside these folders and add the **File-Extension** **`.graphql`**

```text
OPERATIONS/
|   |
|   |-- core/
|   |   `-- methods.graphql --> <File> - Client Code for GraphQL.
|   |
|   `-- etc...
|
`-- etc...
```

And when you run the **Command :** **`schema`**

```sh
./manage.py schema
```

It will **`automatically`** collect all **Operations** and build **5 Files**.

Inside a **Folder** named **`graphql/`**. However, you can **rename** the **`folder/`**.

```yaml title="settings.yaml"
VERSION: 0.1.0
# ... etc

# Rename - Generates (1)
GENERATES: graphql
```

1. **Output** folder for **GraphQL Schema & Operations**.

| #   | File                  | From **`Code`** |
| --- | --------------------- | --------------- |
| 1   | **`schema.graphql`**  | **Python**      |
| 2   | **`core.graphql`**    | **GraphQL**     |
| 3   | **`desktop.graphql`** | **GraphQL**     |
| 4   | **`mobile.graphql`**  | **GraphQL**     |
| 5   | **`operations.json`** | **Python**      |
