!!! warning

    Make sure you read the **Before Starting** documentation.

### Install **Fastberry**

```sh
pdm add "fastberry[testing]"
```

<div id="terminal-getting-started-installation" data-termynal></div>

For the **example above** we used the "testing" option. It will install **`SQL`** and **`Mongo`**.

And **SQL** will be installed with **`SQLite`** that way the only **extra step** you need is to download
<a href="https://www.mongodb.com/try/download/community" target="_blank">**MongoDB**</a>

**However**, is **optional**. You can use **`SQL`** only for **testing purposes**.

!!! note

    **2 Main Options** are available for **fastberry installation**.

    **Mongo**

    ```sh
    pdm add "fastberry[mongo]"
    ```

    **SQL**

    ```sh
    pdm add "fastberry[sql]"
    ```

    ---

!!! info "SQL comes with 3 options"

    ---

    **PostgreSQL**

    ```sh
    pdm add "fastberry[sql]" "databases[postgresql]"
    ```

    **MySQL**

    ```sh
    pdm add "fastberry[sql]" "databases[mysql]"
    ```

    **SQLite**

    ```sh
    pdm add "fastberry[sql]" "databases[sqlite]"
    ```
