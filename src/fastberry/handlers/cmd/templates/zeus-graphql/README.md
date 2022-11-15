# FastBerry **Controller**

---

## Builder

---

### NPM **Installation**

```sh
npm install
```

### NPM **Build**

```sh
npm run build
```

### ECMAScript Module **Distributable (ESM)**

```sh
./dist/lib.mjs
```

---

## Usage

---

### API

```js
import fastberry from "./fastberry.mjs";

const GQL = Fastberry({
	url: "http://localhost:8000/graphql",
	ignore: ["Id"],
});

// Login to API
GQL.api = {
	token: "MySecretToken",
};

// Forms
console.log(GQL.form.forms);
console.log(GQL.form.get("FormSearch"));
console.log(GQL.form.get("Pagination", ["all"])); // Ignores: [all]
console.log(GQL.form.keys("Pagination"));
console.log(GQL.form.labels("Pagination", { all: "all" }));
console.log(GQL.form.labels("Pagination", {}, ["all"])); // Ignore: [all].

// Types
console.log(GQL.type.types);
console.log(GQL.type.get("Product"));
console.log(GQL.type.get("Product", 2, ["category", "group"])); // Depth-Search: [2] and Ignore: [category, group]
console.log(GQL.type.keys("Product"));

// Operations
console.log(GQL.operations.query.keys());
console.log(GQL.operations.mutation.keys());
```

### Zeus-Chain (API)

```js
GQL.api("query");
GQL.api("mutation");
```

### Query

```js
const inputForm = {
	items: GQL.form.get("Item"),
};
const returnType = GQL.type.get("Product");
GQL.api("query")({
	QueryName: [inputForm, returnType],
});
```

### Mutation

```js
const inputForm = {
	items: GQL.form.get("Item"),
};
const returnType = GQL.type.get("Product");
GQL.api("mutation")({
	MutationName: [inputForm, returnType],
});
```

### Python-Style { Dict }

```js
const pyDict = GQL.dict({ msg: "hello world" });

console.log(pyDict.keys());
console.log(pyDict.values());
console.log(pyDict.items());
console.log(pyDict.dict());
console.log(pyDict.dir);
```
