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
|        |-- extension.py
|        |-- graphql.py
|        |-- middleware.py
|        |-- inputs.py
|        |-- permissions.py
|        |-- router.py
|        `-- types.py
|
`-- etc...
```

---

## Application **Diagrams**

=== "GraphQL"

    ### Application **GraphQL**

    ``` mermaid
    graph LR;
        A[Application] --> |GraphQL| B[Operations];
        A --> |Fastberry| C[GraphQL];
        A --> |Strawberry| D[Inputs];
        A --> |Fastberry & Strawberry| E[Types];
    ```

=== "Operations"

    ### Application **Operations**

    ``` mermaid
    graph LR;
        A[Application] --> |GraphQL| B;
        B[Client] --> C[Core]
        B --> D[Desktop]
        B --> E[Mobile]
    ```

=== "Commands"

    ### Application **Commands**

    ``` mermaid
    graph LR;
        A[Application] --> |Click| B[Commands];
    ```

=== "Router"

    ### Application **Router**

    ``` mermaid
    graph LR;
        A[Application] --> |FastAPI| B[Router];
    ```
