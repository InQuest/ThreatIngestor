import threatingestor.artifacts
from threatingestor.operators import Operator
from threatingestor.exceptions import DependencyError


try:
    import pymysql
except ImportError:
    raise DependencyError("Dependency pymysql required for MySQL operator is not installed")


class Plugin(Operator):
    """Operator for MySQL."""
    def __init__(self, host, database, table, user=None, password='', port=3306,
                 artifact_types=None, filter_string=None, allowed_sources=None):
        """MySQL operator."""
        super(Plugin, self).__init__(artifact_types, filter_string, allowed_sources)
        self.artifact_types = artifact_types or [
            threatingestor.artifacts.Domain,
            threatingestor.artifacts.Hash,
            threatingestor.artifacts.IPAddress,
            threatingestor.artifacts.URL,
            threatingestor.artifacts.YARASignature,
            threatingestor.artifacts.Task,
        ]

        # Connect to SQL and set up the tables if they aren't already.
        self.table = table
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

        self._create_table()


    def _create_table(self):
        """Create the table defined in the config if it does not already exist."""
        query = f"""
            CREATE TABLE IF NOT EXISTS `{self.table}` (
                `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `artifact` TEXT,
                `artifact_type` VARCHAR(50),
                `reference_link` TExT,
                `reference_text` TEXT,
                `created_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
                `state` TEXT
            ) 
        """
        # See note in process() on why we connect to SQL here.
        self.sql = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                   password=self.password, database=self.database)
        self.cursor = self.sql.cursor()
        self.cursor.execute(query)
        self.sql.commit()
        self.cursor.close()


    def _insert_artifact(self, artifact):
        """Insert the given artifact into the table."""
        type_name = artifact.__class__.__name__.lower()
        query = f"""
            INSERT IGNORE INTO `{self.table}` (
                `artifact`,
                `artifact_type`,
                `reference_link`,
                `reference_text`,
                `state`
            )
            VALUES (%s, %s, %s, %s, NULL)
        """
        self.cursor.execute(query, (
            str(artifact),
            type_name,
            artifact.reference_link,
            artifact.reference_text
        ))
        self.sql.commit()


    def process(self, artifacts):
        """Override parent method to better handle SQL cursor."""
        # Connect to MySQL and call the parent method.
        # Note: We do this here and in _create_table rather than in the constructor
        # because it seems the SQL connection is prone to timeouts, and
        # establishing the connection here is the most efficient way to avoid that.
        self.sql = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                   password=self.password, database=self.database)
        self.cursor = self.sql.cursor()
        super(Plugin, self).process(artifacts)

        # Close the connection
        self.cursor.close()


    def handle_artifact(self, artifact):
        """Operate on a single artifact."""
        self._insert_artifact(artifact)
