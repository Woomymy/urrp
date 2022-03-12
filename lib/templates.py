"""
Utilities for templates
"""

from os.path import exists
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader

def get_template(filepath: str) -> Template:
    """
    Get a jinja template with full path
    """
    if not exists(filepath):
        raise FileNotFoundError(filepath)
    
    path = Path(filepath)
    parent = str(path.parent.absolute())

    environnement = Environment(loader=FileSystemLoader(parent))

    return environnement.get_template(path.name)
