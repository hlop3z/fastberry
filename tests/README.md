# Fastberry-Todo

Todo Example for **Fastberry**

## Install

```sh
pdm install
```

## Run

```sh
pdm app run
```

## Client

```graphql
fragment ErrorFields on Error {
  error
  meta
  messages {
    field
    text
    type
  }
}

fragment TaskFields on Task {
  id
  title
  description
  status
}

mutation CreateTask {
  create(
    form: {
      title: "First App"
      description: "create an example app."
      status: "open"
    }
  ) {
    ... on Task {
      ...TaskFields
    }
    ... on Error {
      ...ErrorFields
    }
  }
}

mutation CreateSecondTask {
  create(
    form: {
      title: "Post Tutorial"
      description: "post the example app."
      status: "open"
    }
  ) {
    ... on Task {
      ...TaskFields
    }
    ... on Error {
      ...ErrorFields
    }
  }
}

mutation UpdateTask {
  update(item: "MTo6YTU1ZTUzMmVhYjAyOGI0Mg==", status: "close") {
    ... on Task {
      ...TaskFields
    }
    ... on Error {
      ...ErrorFields
    }
  }
}

query AllTasks {
  search(status: null) {
    edges {
      node {
        ...TaskFields
      }
    }
  }
}

query SearchTask {
  search(status: "open") {
    edges {
      node {
        ...TaskFields
      }
    }
  }
}

mutation DeleteTask {
  delete(item: "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ==")
}
```
