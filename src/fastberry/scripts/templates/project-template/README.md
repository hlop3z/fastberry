# Fastberry Template

## Installation

```sh
pdm install
```

## Run Server

```sh
pdm run server
```

## Other Commands

```sh
pdm run manage --help
```

## Secret-Key

---

### Create a **Secret-Key**

> **Optionally**: You can pass a size parameter for example —> `scripts/keygen.sh 64`.

```sh
sh scripts/keygen.sh
```

> After creating the **Secret-Key** add it inside your files.

- config/env/development.env
- config/env/staging.env
- config/env/production.env
