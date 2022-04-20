# Welcome to **Fastberry**

## Links

- ### [PyPi](https://pypi.org/project/dbcontroller)
- ### [Github](https://github.com/hlop3z/dbcontroller)
- ### [Read the Documents](https://hlop3z.github.io/dbcontroller/)

---

## Built With:

- [Click](https://github.com/pallets/click/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Strawberry](https://strawberry.rocks/)
- [Uvicorn](https://www.uvicorn.org/)
- [Gunicorn](https://gunicorn.org/)

---

## Install

---

### Create New Directory

```sh
mkdir my-project
cd my-project/
```

### (PipEnv) Install Fastberry

```sh
python -m pipenv --python 3.10 install fastberry
```

### (PipEnv) Shell

```sh
python -m pipenv shell
```

---

## Start Project

---

### Run (Command) Start-Project

```sh
startproject
```

### Run (Command) Start-App

```sh
./manage.py start-app demo --crud
```

### Inside `settings.yaml`

```yaml
INSTALLED_APPS:
  - demo
```

### Run (Command) Run-Server

```sh
./manage.py run
```
