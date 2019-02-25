import sqlite3


import hug


DATABASE = 'artifacts.sqlite3'


@hug.get('/api/{table}', output=hug.output_format.json)
def list_view(table):
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = [e[0] for e in cursor.fetchmany()]

    if table and table in tables:
        cursor.execute(f'SELECT * FROM {table}')

        data = []
        columns = [c[0] for c in cursor.description]
        for row in cursor.fetchall():
            data.append({k: v for k, v in zip(columns, row)})

        return data

    elif table:
        return f"No table {table}"

    else:
        return tables


@hug.get('/{table}', output=hug.output_format.html)
def html_view(table):
    with open('webapp.html', 'r') as f:
        return f.read()


db = sqlite3.connect(DATABASE)
cursor = db.cursor()
