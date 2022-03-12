#!/usr/bin/env python3

from shutil import copyfile, copytree
from lib.config import load_config
from lib.templates import get_template
from lib.util import check_files, clean_mkdir, mdToHtml

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

    clean_mkdir(config.out_dir)
    
    copyfile(config.zip, f"{config.out_dir}/install-{config.device}.zip")
    copyfile(config.boot, f"{config.out_dir}/boot-{config.device}.img")

    templateParams = {
        "recovery": recovery,
        "marketname": config.prettyname,
        "device": config.device,
        "maintainer": config.maintainer,
        "version": config.release,
        "include_vbmeta": not config.remove_vbmeta
    }

    # We can't directly add them to templateParams, because we need to pass templateParams to generate them
    templateParams["chagenlogHtml"] = mdToHtml(templateParams, config.changelog_path)
    templateParams["installInstructionsHtml"] = mdToHtml(templateParams, config.install_instructions_path)

    template = get_template("templates/index.html.jinja2")
    index = template.render(templateParams)

    with open(f"{config.out_dir}/index.html", 'w') as indexfile:
        indexfile.write(index)
    
    for dir in ["style", "scripts"]:
        print(f"-- Copying {dir} files")
        copytree(dir, f"{config.out_dir}/{dir}")

    if not config.remove_vbmeta:
        copyfile("vbmeta.img", f"{config.out_dir}/vbmeta.img")

if __name__ == "__main__":
    main()
