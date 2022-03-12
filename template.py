#!/usr/bin/env python3
from argparse import ArgumentParser
from distutils.dir_util import copy_tree
from subprocess import run
from jinja2 import Environment, FileSystemLoader
from os import mkdir
from os.path import exists
from shutil import copyfile, rmtree
from lib.config import load_config

def check_files(files: list[str]):
    """
    Check if all required files exist
    """
    for file in files:
        if not exists(file[1]):
            print(f"{file[0]} not found")
            exit(1)

def main():
    config = load_config()
    recovery = "OrangeFox" if config.is_orangefox else "TWRP"

    print(f"Generating {recovery} releases notes for {config.prettyname} ({config.device})")
    # Check if all files exist
    check_files(
        [
            ("Boot image", config.boot),
            ("ZIP Installer", config.zip),
            ("Changelog file", config.changelog_path),
            ("Installation instructions", config.install_instructions_path)
        ]
    )

    htmlChangeLog = run(["pandoc", "-f", "markdown", "-t", "html", config.changelog_path], capture_output=True)
    htmlInstallInstructions = run(["pandoc", "-f", "markdown", "-t", "html", config.install_instructions_path], capture_output=True)
    if exists(config.out_dir):
        rmtree(config.out_dir)

    # Create out dir
    mkdir(config.out_dir)
    
    copyfile(config.zip, f"{config.out_dir}/install-{config.device}.zip")
    copyfile(config.boot, f"{config.out_dir}/boot-{config.device}.img")

    jinja_env = Environment(loader=FileSystemLoader("templates"))

    template = jinja_env.get_template("index.html.jinja2")
    index = template.render(
        recovery=recovery,
        marketname=config.prettyname,
        device=config.device,
        maintainer=config.maintainer,
        version=config.release,
        changelogHtml=htmlChangeLog.stdout.decode("UTF-8"),
        installInstructionsHtml=htmlInstallInstructions.stdout.decode("UTF-8"),
        include_vbmeta=not config.remove_vbmeta
    )

    with open(f"{config.out_dir}/index.html", 'w') as indexfile:
        indexfile.write(index)
    
    print("-- Copying style files")
    copy_tree("style", f"{config.out_dir}/style")
    print("-- Copying script files")
    copy_tree("scripts", f"{config.out_dir}/scripts")

    if not config.remove_vbmeta:
        copyfile("vbmeta.img", f"{config.out_dir}/vbmeta.img")

if __name__ == "__main__":
    main()
