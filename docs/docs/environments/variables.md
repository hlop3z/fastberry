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
	MONGO       = "mongodb://localhost:27017/development"
	SQL         = "sqlite:///development.sqlite3"
	```

	---

	## The **Staging** environment

	```env
	DEBUG       = "yes"
	SECRET_KEY  = "fastapi-insecure-09d25e094faa6ca2556c"
	MONGO       = "mongodb://localhost:27017/staging"
	SQL         = "sqlite:///staging.sqlite3"
	```

	---

	## The **Production** environment

	```env
	DEBUG       = "no"
	SECRET_KEY  = "fastapi-insecure-09d25e094faa6ca2556c"
	MONGO       = "mongodb://localhost:27017/production"
	SQL         = "sqlite:///production.sqlite3"
	```

=== "Variables"

	## **Variables**

	> The environment **variables**.

	- **DEBUG**: yes | no
	- **SECRET_KEY**: Secret-Api-Key
	- **MONGO (URI)**: mongodb://localhost:27017/myDatabaseName
	- **SQL (URI)**: sqlite:///myDatabaseName.sqlite3

	---

	## Demo **Environment**

	```env
	DEBUG       = "yes"
	SECRET_KEY  = "fastapi-insecure-09d25e094faa6ca2556c"
	MONGO       = "mongodb://localhost:27017/staging"
	SQL         = "sqlite:///staging.sqlite3"
	```

	---

	## Engines

	- **Mongo** uses [Motor](https://pypi.org/project/motor/)
	- **SQL** uses [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)

	---

	## **mode**.json

	> The file **mode.json** is updated **automatically** when you run the server in a specific mode.

	```json
	{
		"mode": "development"
	}
	```
