import json

import jsonpath_rw

from threatingestor.sources import Source

class AbstractPlugin(Source):

    def __init__(self, name, paths, reference=None):
        """Args should be url, auth, etc, whatever is needed to set up the object.

        The name argument is required for all Source plugins, and is used internally.
        """
        self.name = name
        # Parse paths into path expressions.
        self.path_expressions = [jsonpath_rw.parse(path) for path in paths]
        # Try to parse reference as a path, fall back to name.
        self.reference = jsonpath_rw.parse(reference) if reference else name

    def get_objects(self, saved_state):
        """Produce an iterable of dict or list objectcs containing raw content to process.

        Override in child class."""
        raise NotImplementedError()

    def run(self, saved_state):
        """Run and return (saved_state, list(Artifact))"""
        artifact_list = []

        for content in self.get_objects(saved_state):
            # Iterate over each piece of "content", extracting from every path of interest.
            for path_expression in self.path_expressions:
                matches = path_expression.find(content)

                # Try to get a single reference, fall back to name again.
                try:
                    reference = self.reference.find(content)[0].value
                except IndexError:
                    reference = self.name

                # Extract artifacts.
                for match in matches:
                    artifact_list += self.process_element(match.value, reference, include_nonobfuscated=True)

        return saved_state, artifact_list
