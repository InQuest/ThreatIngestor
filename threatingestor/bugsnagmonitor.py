import bugsnag

def configure_bugsnag(api_key=None) -> bool:
    """
    Configure BugSnag API communication in `config.yml`.
    """

    if api_key:
        bugsnag.configure(api_key=api_key)
        return True

    return False

def send_notification(msg=None, metadata=None) -> None:
    """
    Monitor your code with BugSnag

    You can include a additional information with the `metadata` paramater.
    """
    bugsnag.notify(Exception(msg), metadata={"ThreatIngestor" : metadata})
