> There are **two-ways** in which you can start using **fastberry**.
>
> 1. **Installing** and **Starting** a new Project.
> 2. **Download** the template.

---

## Installation

---

### Create **New Directory**

```sh
mkdir my-project
cd my-project/
```

### Initiate (**PDM**)

```sh
pdm init
```

### Install **Fastberry + Uvicorn** (PDM)

```sh
pdm add fastberry "uvicorn[standard]"
```

### Start a **Project**

```sh
pdm run startproject
```

### Run **Server**

```sh
pdm run python manage.py run
```

---

## Start an **App**

---

### Run (**`command`**) **Start-App**

```sh
pdm run python manage.py start-app demo --crud
```

### Inside **`settings.yaml`**

```yaml title="settings.yaml"
INSTALLED_APPS:
  - demo
```

---

## Run **Server**

---

### Run (**`command`**) **Run-Server**

```sh
pdm run python manage.py run
```

---

## Add Development **Tools**

---

```
pdm add -dG devops isort black pylint bandit watchdog pre-commit
```
