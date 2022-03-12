#!/usr/bin/env python3

from shutil import copyfile, copytree
from lib.config import load_config
from lib.templates import get_template
from lib.util import check_files, clean_mkdir, mdToHtml, write_sha256


def main():
    config = load_config()
    recovery = "OrangeFox" if config.is_orangefox else "TWRP"

    print(
        f"Generating {recovery} releases notes for {config.prettyname} ({config.device})")

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
    templateParams = {
        "recovery": recovery,
        "marketname": config.prettyname,
        "device": config.device,
        "maintainer": config.maintainer,
        "version": config.release,
        "include_vbmeta": not config.remove_vbmeta
    }

    # We can't directly add them to templateParams, because we need to pass templateParams to generate them
    templateParams["changelogHtml"] = mdToHtml(
        templateParams, config.changelog_path)
    templateParams["installInstructionsHtml"] = mdToHtml(
        templateParams, config.install_instructions_path)

    template = get_template("templates/index.html.jinja2")
    index = template.render(templateParams)

    with open(f"{config.out_dir}/index.html", 'w') as indexfile:
        indexfile.write(index)

    copytree("style", f"{config.out_dir}/style")

    zipOut = f"{config.out_dir}/install-{config.device}.zip"
    bootOut = f"{config.out_dir}/boot-{config.device}.img"

    print("-- Copying installer and boot image")
    copyfile(config.zip, zipOut)
    copyfile(config.boot, bootOut)

    print("-- Generating SHA256 files")
    write_sha256(zipOut)
    write_sha256(bootOut)

    if not config.remove_vbmeta:
        print("-- Copying VBMeta and sha256sum")
        vbmetaOut = f"{config.out_dir}/vbmeta.img"
        copyfile("vbmeta.img", vbmetaOut)
        write_sha256(vbmetaOut)


if __name__ == "__main__":
    main()
