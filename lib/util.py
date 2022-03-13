"""
Various utilities
"""

from hashlib import sha256
from os.path import exists
from os import mkdir
from sys import exit as sexit
from subprocess import run
from shutil import rmtree
from lib.templates import get_template


def check_files(files: list[str]):
    """
    Check if all required files exist
    """
    for file in files:
        if not exists(file[1]):
            print(f"{file[0]} not found")
            sexit(1)


def clean_mkdir(path: str):
    """
    Create an empty dir and clean it if it already exists
    """

    if exists(path):
        rmtree(path)

    mkdir(path)


def md_to_html(template_params: dict[str, str], file: str) -> str:
    """
    Run jinja on a template, and convert it to HTML using pandoc
    """

    template_jinja = get_template(file).render(template_params)

    # pass string directly in stdin
    return run([
        "pandoc",
        "-f",
        "markdown",
        "-t",
        "html",
    ], check=True, capture_output=True, input=template_jinja.encode()).stdout.decode("UTF-8")


def write_sha256(filepath: str):
    """
    Write files sha256 sum in {file}.sha256sum
    """
    out = f"{filepath}.sha256sum"
    file_hash = sha256()

    with open(filepath, "rb") as input_file:
        for fbytes in iter(lambda: input_file.read(4096), b""):
            file_hash.update(fbytes)

    print(f"--- {filepath}.sha256: {file_hash.hexdigest()}")

    with open(out, "w", encoding="UTF-8") as out_file:
        out_file.write(f"{file_hash.hexdigest()}\n")


def gpg_sign(files: list[str], opts: str):
    """
    Sign a list of files with gpg (use "opts" to add more CLI arguments)
    """
    cmd = "gpg"
    if opts != "":
        # Add a space just in case
        cmd += f" {opts}"

    cmd += " --detach-sig {file}"

    for file in files:
        print(f"--- Signing {file}")
        run(cmd.format(file=file).split(' '), check=True)
