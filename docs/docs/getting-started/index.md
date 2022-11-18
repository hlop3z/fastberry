!!! warning

    For the tutorial there is an **extra requirement**.

## <a href="https://pypi.org/project/pdm/" target="_blank">**P**ython **D**ependencies **M**anager</a>

First of all take a look at the tool <a href="https://pypi.org/project/pdm/" target="_blank">**PDM**</a>. Because, we will use it to build our **First API**.

### **PDM** For **Linux/Mac**

```sh
curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -
```

### **PDM** For **Windows**

```sh
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py -UseBasicParsing).Content | python -
```

## Getting Started

!!! warning

    **Bash** required. If you are in a **Windows** computer take a look at <a href="https://gitforwindows.org/" target="_blank">**Git BASH**</a>.

### Create a Folder

```sh
mkdir myproject
cd myproject/
```

### Init **PDM**

```sh
pdm init
```

!!! note

    We **selected** Number "**`1`**" in order to use python version (**`3.10`**)

    The **output** in your computer will look similar but **not exactly the same**.

<div id="terminal-getting-started" data-termynal></div>

!!! note

    Then **continue** with the setup.

<div id="terminal-getting-started-2" data-termynal></div>
