> There are **two-ways** in which you can start using **fastberry**.
>
> 1. **Installing** and **Starting** a new Project.
> 2. **Download** the template and use **pipenv** to recreate the environment.

## Installation

---

### Create **New Directory**

```sh
mkdir my-project
cd my-project/
```

### (PipEnv) Install **Fastberry + Uvicorn**

```sh
python -m pipenv --python 3.10 install fastberry "uvicorn[standard]"
```

### (PipEnv) **Shell**

```sh
python -m pipenv shell
```

---

## Start **Project**

---

### Run (Command) **Start-Project**

> Make sure you created a new **`directory/`**. Because the **`startproject`** command creates the files in the **CURRENT** **`directory/`**

```sh
startproject
```

## Start **App**

---

### Run (**`command`**) **Start-App**

```sh
./manage.py start-app demo --crud
```

### Inside **`settings.yaml`**

```yaml title="settings.yaml"
INSTALLED_APPS:
  - demo
```

## Run **Server**

---

### Run (**`command`**) **Run-Server**

```sh
./manage.py run
```
