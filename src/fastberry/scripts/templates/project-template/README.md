# Fastberry Template

$~~$

## Virtual Environment

---

### (PipEnv) Shell

```sh
python -m pipenv shell
```

### Run Server

```sh
./manage.py run
```

### More Commands

```sh
./manage.py --help
```

$~~$

## Dependencies Management

---

### (PipEnv) Recreate in **Development**

```sh
python -m pipenv install --dev --skip-lock
```

### (PipEnv) Recreate in **Production**

```sh
python -m pipenv install --ignore-pipfile
```

$~~$

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
