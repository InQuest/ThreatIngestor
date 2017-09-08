from __future__ import absolute_import

import csv

import artifacts
from operators import Operator

class CSV(Operator):
    """Operator for output to flat CSV file"""

    def __init__(self, filename):
        """CSV operator"""
        self.filename = filename

        self.artifact_types = [artifacts.Domain, artifacts.IPAddress, artifacts.URL]

    def handle_artifact(self, artifact):
        """Operate on a single artifact"""
        with open(self.filename, 'a+') as f:
            writer = csv.writer(f)
            artifact_type = unicode(artifact.__class__).split('.')[-1].encode('utf-8')
            writer.writerow([artifact_type, unicode(artifact).encode('utf-8'),
                    artifact.reference_link.encode('utf-8'),
                    artifact.reference_text.encode('utf-8').encode('string_escape')])
