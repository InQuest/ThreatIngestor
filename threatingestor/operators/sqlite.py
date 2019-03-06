from __future__ import absolute_import
import sqlite3


import threatingestor.artifacts
from threatingestor.operators import Operator


class Plugin(Operator):
    """Operator for SQLite3."""
    def __init__(self, filename, artifact_types=None, filter_string=None, allowed_sources=None):
        """SQLite3 operator."""
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
        self.sql = sqlite3.connect(filename)
        self.cursor = self.sql.cursor()

        self._create_tables()


    def _create_tables(self):
        """Create tables for each supported artifact type."""
        for artifact_type in self.artifact_types:
            type_name = artifact_type.__name__.lower()
            query = f"""
                CREATE TABLE IF NOT EXISTS `{type_name}` (
                    `artifact` TEXT PRIMARY KEY,
                    `reference_link` TExT,
                    `reference_text` TEXT,
                    `created_date` TEXT,
                    `state` TEXT
                )
            """
            self.cursor.execute(query)
        self.sql.commit()


    def _insert_artifact(self, artifact):
        """Insert the given artifact into its corresponding table."""
        type_name = artifact.__class__.__name__.lower()
        query = f"""
            INSERT OR IGNORE INTO `{type_name}` (
                `artifact`,
                `reference_link`,
                `reference_text`,
                `created_date`,
                `state`
            )
            VALUES (?, ?, ?, datetime('now', 'utc'), NULL)
        """
        self.cursor.execute(query, (
            str(artifact),
            artifact.reference_link,
            artifact.reference_text
        ))
        self.sql.commit()


    def handle_artifact(self, artifact):
        """Operate on a single artifact."""
        self._insert_artifact(artifact)
