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
----------

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

- Assets: Images & Icons for frontend
- Configs: Seeds for Database setup
- Logs: All Appreciation logs goes to here
- Messages: All Instruction & Guidance goes to here
- Utils: Supportive functionalities for the website **(BEWARE TO MODIFY)**

## Asset Management

Files placed inside the `assets` directory and its subdirectories (excluding `js` and `css`) will be copied by webpack's `file-loader` into the `static/build` directory, with hashes of their contents appended to their names. For instance, if you have the file `assets/img/favicon.ico`, this will get copied into something like `static/build/img/favicon.fec40b1d14528bf9179da3b6b78079ad.ico`. You can then put this line into your header:

```html
<link rel="shortcut icon" href="{{asset_url_for('img/favicon.ico') }}">
```

to refer to it inside your HTML page. If all of your static files are managed this way, then their filenames will change whenever their contents do, and you can ask Flask to tell web browsers that they should cache all your assets forever by including the following line in your `settings.py`:

```py
SEND_FILE_MAX_AGE_DEFAULT = 31556926  # one year
```
