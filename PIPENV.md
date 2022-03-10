# Run

## Venv **Run** 
```sh
python -m pipenv run some_command_inside_venv
```

## Venv **Shell**
```sh
python -m pipenv shell
```

<br /><br />

# Install

## Install to **Core** 
```sh
python -m pipenv install {package_or_module_name}
```


## Install to **Development** 
```sh
python -m pipenv install {package_or_module_name} --dev
```

<br /><br />

# Save

## Save **Requirements** for Production & Development 
```sh
python -m pipenv lock
```

<br /><br />

# Recreate

## Recreate in **Production** 
```sh
python -m pipenv install --ignore-pipfile
```


## Recreate in **Development** 
```sh
python -m pipenv install --dev
```

<br /><br />

# Others

## Detection of **Security Vulnerabilities**
```sh
python -m pipenv check
```

## Tree-like structure **Dependencies**
```sh
python -m pipenv graph
```
