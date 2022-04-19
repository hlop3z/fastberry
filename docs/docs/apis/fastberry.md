# Fastberry **API**

The **API** can **only** be used **inside** your **`functions`**.
However, it can be initialized **outside** your **`functions`**.

## Python **Code**

```python
from fastberry import Fastberry

manager = Fastberry()
```

## API **Usage**

```python
print(manager.mode)
```

| Key              | File                | Description                                                                             |
| ---------------- | ------------------- | --------------------------------------------------------------------------------------- |
| **`mode`**       | **`mode.json`**     | (**`str`**) — API's Current **Mode** (**`development`, `staging`, `production`**)       |
| **`env`**        | **`mode.env`**      | (**`object`**) — **Environment** Variables (**`development`, `staging`, `production`**) |
| **`base`**       | **`settings.yaml`** | (**`object`**) — Project Core **Settings**                                              |
| **`base_dir`**   | `None`              | (**`path`**) — Project Core **Directory**                                               |
| **`debug`**      | `None`              | (**`bool`**) — Debug **Mode**                                                           |
| **`models`**     | `None`              | (**`dict`**) — Database(s) **Models** accessed by using **`App_Name.Model_Name`**       |
| **`secret_key`** | `None`              | (**`str`**) — **`Secret Key`** is used to provide **cryptographic** signing.            |

---

## API **Backend**

> Everything in the section below is **automatically** placed inside your project's **code**. Mostly inside your **`main.py`** or **`manage.py`**

| Key              | Description                            |
| ---------------- | -------------------------------------- |
| **`apps`**       | All **apps** get loaded here           |
| **`cli`**        | All **commands** get loaded here       |
| **`docs`**       | The **documentation** gets loaded here |
| **`extensions`** | All **extensions** get loaded here     |
| **`middleware`** | All **middleware** gets loaded here    |
| **`router`**     | All **routers** get loaded here        |
