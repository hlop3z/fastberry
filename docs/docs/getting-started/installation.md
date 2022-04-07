> There are **two-ways** in which you can start using **fastberry**.
>
> 1. **Installing** and **Starting** a new Project.
> 2. **Download** the template and use **pipenv** to recreate the environment.

## Installation

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

### Run (Command) **Start-Project**

```sh
startproject
```

## Start App

---

### Run (Command) **Start-App**

```sh
./manage.py start-app demo
```

### Inside **`settings.yaml`**

```yaml
INSTALLED_APPS:
  - demo
```

## Run Server

---

### Run (Command) **Run-Server**

```sh
./manage.py run
```
