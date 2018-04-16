from __future__ import absolute_import

import csv

import artifacts
from operators import Operator

class CSV(Operator):
    """Operator for output to flat CSV file"""

    def __init__(self, filename, artifact_types=None, filter_string=None, allowed_sources=None):
        """CSV operator"""
        self.filename = filename

        super(CSV, self).__init__(artifact_types, filter_string, allowed_sources)
        self.artifact_types = artifact_types or [
            artifacts.Domain,
            artifacts.IPAddress,
            artifacts.URL,
        ]

    def handle_artifact(self, artifact):
        """Operate on a single artifact"""
        with open(self.filename, 'a+') as f:
            writer = csv.writer(f)
            artifact_type = unicode(artifact.__class__).split('.')[-1].encode('utf-8')
            writer.writerow([artifact_type, unicode(artifact).encode('utf-8'),
                    artifact.reference_link.encode('utf-8'),
                    artifact.reference_text.encode('utf-8').encode('string_escape')])
