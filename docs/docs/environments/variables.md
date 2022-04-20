# Environment(s) Variables

=== "Environments"

    ## **Environments**

    > Create **different** environment **`variables`** (aka: **settings**). For each **`stage`** of your **API**.
    >
    > - Development
    - Staging
    - Production

    ## The **Development** environment

    ```env
    DEBUG       = "yes"
    SECRET_KEY  = "fastapi-insecure-09d25e094faa6ca2556c"
    ```

    ---

    ## The **Staging** environment

    ```env
    DEBUG       = "yes"
    SECRET_KEY  = "fastapi-insecure-09d25e094faa6ca2556c"
    ```

    ---

    ## The **Production** environment

    ```env
    DEBUG       = "no"
    SECRET_KEY  = "fastapi-insecure-09d25e094faa6ca2556c"
    ```

=== "Variables"

    ## **mode**.json

    > The file **mode.json** is updated **automatically** when you run the server in a specific **`mode`**.

    ```json
    {
    	"mode": "development"
    }
    ```

    ---

    ## **Variables**

    > The environment **variables**.

    - **DEBUG**: yes | no
    - **SECRET_KEY**: Your-Secret-Api-Key

    ---

    ## Demo **Environment**

    ```env
    DEBUG       = "yes"
    SECRET_KEY  = "fastapi-insecure-09d25e094faa6ca2556c"
    ```
