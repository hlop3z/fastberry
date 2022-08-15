# Welcome to **Fastberry**

## Links

- ### [PyPi](https://pypi.org/project/fastberry)
- ### [Github](https://github.com/hlop3z/fastberry)
- ### [Read the Documents](https://hlop3z.github.io/fastberry/)

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

### Run (Command) Init PDM

```sh
python -m pdm init
```

### (PDM) Install Fastberry

```sh
python -m pdm add fastberry "uvicorn[standard]"
```

---

## Start Project

---

### Run (Command) Start-Project

```sh
python -m pdm run startproject
```

### Run (Command) Start-App

```sh
python -m pdm run python ./manage.py start-app demo --crud
```

### Inside `settings.yaml`

```yaml
INSTALLED_APPS:
  - demo
```

### Run (Command) Run-Server

```sh
python -m pdm run python ./manage.py run
```
