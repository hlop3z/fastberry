# Introduction

> The **Application** definition in **`Fastberry`** is basically a python **`module`**.

The **idea** is to have "self-contained" **`blocks of code`** that are **reusable**.

Also, easy to **share** and use **inside** other **`Fastberry`** projects.

---

## Command

```sh
./manage.py start-app my_awesome_app
```

---

## Files **Layout**

```text
root/
|
|--  apps/
|    `--  MY_APPLICATION/       --> <Directory> - Your App in HERE!
|        |-- operations/        --> <Directory> - GraphQL-Operations in HERE!
|        |-- __init__.py
|        |-- commands.py
|        |-- crud.py
|        |-- extension.py
|        |-- middleware.py
|        |-- inputs.py
|        |-- models.py
|        |-- permissions.py
|        |-- router.py
|        `-- types.py
|
`-- etc...
```

---

## Application **Diagrams**

=== "CRUD"

    ### Application **CRUD**

    ``` mermaid
    graph LR;
        A[Application] --> |GraphQL| B[Operations];
        A --> |Fastberry| C[CRUD];
        A --> |Strawberry| D[Inputs];
        A --> |Databases| E[Models];
        A --> |Strawberry| F[Types];
    ```

=== "Router"

    ### Application **Router**

    ``` mermaid
    graph LR;
        A[Application] --> |FastAPI| B[Router];
    ```

=== "Commands"

    ### Application **Commands**

    ``` mermaid
    graph LR;
        A[Application] --> |Click| B[Commands];
    ```
