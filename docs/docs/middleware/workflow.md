# Middleware + Extension + Permissions

Building a plugin with all **3 elements** (Middleware, Extension and Permissions).

> You can also **combine** them with a **`Router`**. For example: to create a **`User / Authentication`** API.

---

## Plugin **Workflow**

```mermaid
graph LR;
    Z[Client] --> A;
    A[Request] --> B;
    B{Middleware} --> C;
    C{Extension} --> D;
    D{Permissions} --> E;
    E[Resolver] --> F;
    F[Response] --> Z;
```

---

## **Middleware** (FastAPI / Starlette)

> User is **`Authenticated`** or **`Anonymous`**?
>
> Inject the **`Authorization Token`** to the **`Headers`** if the is in the **`Cookies`**.

```mermaid
graph LR;
    A{My Middleware} --> |Request Headers| B[Authorization Token?];
    B --> |Yes| D[Authenticated-User];
    B --> |No| C[Authorization Cookie?];
    C --> |No| E[Anonymous-User];
    C --> |Yes| F[Inject-Header];
    F --> |Authorization Token| B;
    D --> Z[Resolver / Next-Method];
    E --> Z;
```

---

## **Extension** (Strawberry)

> Convert **`Authorization-Token`** or **`None`** to a **`User-Object`** and inject it to **`GraphQL`**'s context.

```mermaid
graph LR;
    A{My Extension} --> |Request:Headers| B;
    B[Authorization Token?] --> |Yes| C[Authenticated-User];
    B --> |No| D[Anonymous-User];
    C --> E[User-Object];
    D --> E;
    E --> |Inject User| F[info.context];
    F --> Z[Resolver / Next-Method];;
```

---

## **Permissions** (Strawberry)

> Get the request's **`User`** and check the **`Role`** for a **list of allowed methods**.
>
> Then, check if **`info.field_name`** (which is the name of the current: **`Query`** or **`Mutation`**) is in the **list of allowed methods**.
>
> Alternatively, you can use **`info.python_name`** if you prefer to use the python's original name of the function.

```mermaid
graph LR;
    A{My Permission} --> |info.context| B[User];
    B --> |is| C[Allowed?]
    C --> |Yes| F[Resolver / Next-Method]
    C --> |No| G[Response: Error]
```
