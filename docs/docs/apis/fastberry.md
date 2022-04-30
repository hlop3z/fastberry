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
| **`secret_key`** | `None`              | (**`str`**) — **`Secret Key`** is used to provide **cryptographic** signing.            |

---

## API **Backend**

> Everything in the section below is **automatically** placed inside your project's **code**. Mostly inside your **`main.py`** or **`manage.py`**

| Key              | Description                                                 |
| ---------------- | ----------------------------------------------------------- |
| **`apps`**       | All **Apps** get loaded here                                |
| **`cli`**        | All **Commands** get loaded here                            |
| **`docs`**       | The **Documentation** gets loaded here                      |
| **`types`**      | All **Types** get loaded here                               |
| **`extensions`** | All **Extensions** get loaded here                          |
| **`middleware`** | All **Middleware** gets loaded here                         |
| **`router`**     | All **Routers** get loaded here                             |
| **`on_event`**   | All **`ON_STARTUP`** and **`ON_SHUTDOWN`** gets loaded here |
