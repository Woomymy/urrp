from os.path import exists
from os import mkdir
from subprocess import run
from shutil import rmtree
from lib.templates import get_template

"""
Various utilities
"""

def check_files(files: list[str]):
    """
    Check if all required files exist
    """
    for file in files:
        if not exists(file[1]):
            print(f"{file[0]} not found")
            exit(1)

def clean_mkdir(path: str):
    """
    Create an empty dir and clean it if it already exists
    """

    if exists(path):
        rmtree(path)

    mkdir(path)

def mdToHtml(templateParams: dict[str, str], file: str) -> str:
    """
    Run jinja on a template, and convert it to HTML using pandoc
    """

    templateJinja = get_template(file).render(templateParams)

    # pass string directly in stdin
    return run([
        "pandoc",
        "-f",
        "markdown",
        "-t",
        "html",
    ], capture_output=True, input=templateJinja.encode()).stdout.decode("UTF-8")
