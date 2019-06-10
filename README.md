# Weather Case Simulator (wxcs)

Severe weather case simulator

## Quickstart

Run the following commands to bootstrap your environment :

```bash
git clone https://github.com/darekaze/wxcs
cd wxcs
pipenv install -d
pipenv run flask run
```

You will see a pretty welcome screen.

Once you have installed your DBMS, run the following to create your app's database tables and perform the initial seeding:

```bash
flask db upgrade
flask seed
flask sync
pipenv run flask run
```

## Creating the view

```sql
CREATE VIEW v_toolsets AS 
SELECT t.*, l.name, l.href 
FROM toolsets AS t 
JOIN links AS l ON t.link_id = l.id
```

## Going Production Mode

In your production environment, make sure the `FLASK_DEBUG` environment variable is unset or is set to `0`. In your `.env` file:

```bash
FLASK_ENV=production
FLASK_DEBUG=0
DATABASE_URL="<PRODUCTION DATABASE URL>"
```

## Shell

To open the interactive shell, run :

```bash
flask shell
```

By default, you will have access to the flask `app`.

## Migrations

Whenever a database migration needs to be made. Run the following commands :

```bash
flask db migrate
```

This will generate a new migration script. Then run :

```bash
flask db upgrade
```

To apply the migration.

For a full migration command reference, run `flask db --help`.

## Static Folder

- Assets
  - Icons: Images & Icons for frontend
  - Logs: Appreciation logs
  - Messages: Instruction & Guidance
- Configs: Seeds for Database setup
- Utils: Supportive functionalities for the website **(BEWARE TO MODIFY)**
