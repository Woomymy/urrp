#!/usr/bin/env python3
from argparse import ArgumentParser
from distutils.dir_util import copy_tree
from subprocess import run
from jinja2 import Environment, FileSystemLoader
from os import mkdir
from os.path import exists
from shutil import copyfile, rmtree

def check_files(files):
    """
    Check if all required files exist
    """
    for file in files:
        if not exists(file[1]):
            print(f"{file[0]} not found")
            exit(1)

def main():
    cli = ArgumentParser(description="Generate site template")
    cli.add_argument('--device', type=str, help="Device codename", required=True)
    cli.add_argument('--prettyname', type=str, help="Device market/pretty name", required=True)
    cli.add_argument('--boot', type=str, help="Boot/recovery image", required=True)
    cli.add_argument('--zip', type=str, help="ZIP installer", required=False, default="")
    cli.add_argument('--remove-vbmeta', type=bool, help="Don't include vbmeta image", default=False)
    cli.add_argument('--out-dir', type=str, help="Output directory", required=False, default="out")
    cli.add_argument('--release', type=str, help="Release version", required=True)
    cli.add_argument('--is-orangefox', type=bool, help="OrangeFox build", required=False, default=False)
    cli.add_argument('--maintainer', type=str, help="Maintainer name", required=True)
    cli.add_argument('--changelog', type=str, help="Changelog file", required=True)
    cli.add_argument('--install-instructions', type=str, help="Installation instructions", required=True)

    args = cli.parse_args()
    recovery = "OrangeFox" if args.is_orangefox else "TWRP"

    print(f"Generating {recovery} releases notes for {args.prettyname} ({args.device})")
    # Check if all files exist
    check_files(
        [
            ("Boot image", args.boot),
            ("ZIP Installer", args.zip),
            ("Changelog file", args.changelog),
            ("Installation instructions", args.install_instructions)
        ]
    )

    htmlChangeLog = run(["pandoc", "-f", "markdown", "-t", "html", args.changelog], capture_output=True)
    htmlInstallInstructions = run(["pandoc", "-f", "markdown", "-t", "html", args.install_instructions], capture_output=True)
    if exists(args.out_dir):
        rmtree(args.out_dir)

    # Create out dir
    mkdir(args.out_dir)
    
    copyfile(args.zip, f"{args.out_dir}/install-{args.device}.zip")
    copyfile(args.boot, f"{args.out_dir}/boot-{args.device}.img")

    jinja_env = Environment(loader=FileSystemLoader("templates"))

    template = jinja_env.get_template("index.html.jinja2")
    index = template.render(
        recovery=recovery,
        marketname=args.prettyname,
        device=args.device,
        maintainer=args.maintainer,
        version=args.release,
        changelogHtml=htmlChangeLog.stdout.decode("UTF-8"),
        installInstructionsHtml=htmlInstallInstructions.stdout.decode("UTF-8"),
        include_vbmeta=not args.remove_vbmeta
    )

    with open(f"{args.out_dir}/index.html", 'w') as indexfile:
        indexfile.write(index)
    
    print("-- Copying style files")
    copy_tree("style", f"{args.out_dir}/style")
    print("-- Copying script files")
    copy_tree("scripts", f"{args.out_dir}/scripts")

    if not args.remove_vbmeta:
        copyfile("vbmeta.img", f"{args.out_dir}/vbmeta.img")

if __name__ == "__main__":
    main()
