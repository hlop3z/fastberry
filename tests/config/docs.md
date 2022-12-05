# Welcome

> This is a simple **API** Skeleton

---

## Links

> Go To [GraphQL](/graphql)

---

## Mode (Options)

- `development`

- `staging`

- `production`

---

## Settings Layout

```text
root/                           --> <Directory> - Project's Root.
|
|--  config/                    --> <Directory> - Configurations.
|    |
|    |-- .env/                  --> <Directory> - Environments.
|    |   |
|    |   |-- development.toml   --> <File> - Development    | Settings.
|    |   |-- production.toml    --> <File> - Production     | Settings.
|    |   `-- staging.toml       --> <File> - Staging        | Settings.
|    |
|    |-- docs.md                --> <File> - This Documentation is in HERE.
|    |-- settings.py            --> <File> - Python         | Settings.
|    `-- spoc.toml              --> <File> - TOML           | Settings.
|
|-- pyproject.toml              --> <File> - Project        | Settings.
|
`-- etc...
```