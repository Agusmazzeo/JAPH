
class ConfigNotFound(Exception):
    """Exception raised when a given config file is not found"""

class ProjectNotFound(Exception):
    """Exception raised when a given project is not found in the config file"""

class RepeatedProjectName(Exception):
    """Exception raised when the given project name is repeated in the config file"""

class IncompleteConfigFile(Exception):
    """Exception raised when a config file is incomplete"""