The environment **variables**.

- **DEBUG**: Yes | No
- **SECRET_KEY**: Secret-Api-Key
- **MONGO (URI)**: mongodb://localhost:27017/myDatabaseName
- **SQL (URI)**: sqlite:///myDatabaseName.sqlite3

---

## Engines

- **Mongo** uses Motor
- **SQL** uses SQLAlchemy

---

## **mode**.json

> The file **mode.json** is updated **automatically** when you run the server in a specific mode.

```json
{
	"mode": "development"
}
```

---

## Locations

```text
root/                           --> <Directory> - Project's Root.
|
|--  config/                    --> <Directory> - Configurations.
|    |-- etc...
|    |-- env/                   --> <Directory> - Environments.
|    |   |-- development.env    --> <File> - Development Settings.
|    |   |-- production.env     --> <File> - Production Settings.
|    |   `-- staging.env        --> <File> - Staging Settings.
|    |
|    `-- mode.json              --> <File> - Current Mode.
|
`-- etc...
```
