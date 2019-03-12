import sqlite3


import hug


DATABASE = 'artifacts.db'


INDEX_HTML = """
<html>
<head>
    <script
      src="https://code.jquery.com/jquery-3.3.1.min.js"
      integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
      crossorigin="anonymous"></script>

    <script type="text/javascript">
        $(document).ready(function() {
            $.ajax('/api/index').done(function(tables) {
                tables.forEach(function(table) {
                    $("body").append(`<p><a href="/${table}">${table}</a></p>`);
                });
            });
        });
    </script>
</head>
<body>
<h1>Artifact types</h1>
</body>
</html>
"""


LIST_HTML = """
<html>
<head>
    <script
      src="https://code.jquery.com/jquery-3.3.1.min.js"
      integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
      crossorigin="anonymous"></script>
      <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/dt/dt-1.10.18/datatables.min.css"/>

    <script type="text/javascript" src="https://cdn.datatables.net/v/dt/dt-1.10.18/datatables.min.js"></script>
    <script type="text/javascript">
        $(document).ready(function() {
            $('#table').DataTable({
                "ajax": {
                    "url": `/api${window.location.pathname}`,
                    "dataSrc": "",
                },
                "columns": [
                    {"data": "artifact"},
                    {"data": "reference_link"},
                    {"data": "reference_text"},
                    {"data": "created_date"},
                    {"data": "state"}
                ]
            });
        });
    </script>

</head>
<body>
    <table id='table'>
        <thead>
            <tr>
                <th>Artifact</th>
                <th>Reference Link</th>
                <th>Reference Text</th>
                <th>Created Date</th>
                <th>State</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>
</body>
</html>
"""


@hug.get('/api/{table}', output=hug.output_format.json)
def list_view(table):
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = [e[0] for e in cursor.fetchall()]

    if table == 'index':
        return tables

    elif table and table in tables:
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
    if table:
        return LIST_HTML
    else:
        return INDEX_HTML


db = sqlite3.connect(DATABASE)
cursor = db.cursor()


if __name__ == "__main__":
    print("usage: hug -m threatingestor.extras.webapp")
