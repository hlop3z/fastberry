# FastBerry (ESM)

## Init the **API**

```js
import client from "./client";

const api = client({
  url: "http://localhost:8000/graphql",
  debug: true,
  maxDepth: 6,
  config: {
    mode: "cors",
    credentials: "same-origin", // same-origin include
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json; charset=UTF-8",
    },
  },
});

// Pre-Built { Query(s) & Mutation(s) } from { Schema }
console.log(api.admin.keys);
```

---

## How To **Disable Fields**

```js
// Single Model
const instance = api.gql("query", "MyQuery", ["Id"]);

// Edge Model
const instance = api.gql("query", "MyQuery", ["edges.node.Id"]); // Recursive Disable ["via.dots"]

// Multi Model
const instance = api.gql("mutation", "MyMutation", { Model: ["Id"] });
```

---

## **GQL** Request Demo

```js
// Init (Editable) Instance
const instance = api.gql("query", "MyQuery", ["Id"]);

// Edit
instance.form.item = "MTo6YTU1ZTUzMmVhYjAyOGI0Mg==";

// Run
const { MyQuery } = await instance.run(instance);

console.log(MyQuery);
```

---

## **Chain** Request Demo

```js
const request = {
  MyQuery: [
    // Response
    {
      id: true,
      name: true,
    },
    // Inputs
    {
      item: "MTo6YTU1ZTUzMmVhYjAyOGI0Mg==",
    },
  ],
};

api.chain("query", request).then((response) => {
  console.log(response);
});
```
