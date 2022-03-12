#!/usr/bin/env python3
"""
Generate static site for TWRP/OrangeFox official releases
"""

from shutil import copyfile, copytree
from lib.config import load_config
from lib.templates import get_template
from lib.util import check_files, clean_mkdir, md_to_html, write_sha256


def main():
    """
    Main function
    """
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
    template_params = {
        "recovery": recovery,
        "marketname": config.prettyname,
        "device": config.device,
        "maintainer": config.maintainer,
        "version": config.release,
        "include_vbmeta": not config.remove_vbmeta
    }

    # We can't directly add them to templateParams
    # because we need to pass templateParams to generate them
    template_params["changelogHtml"] = md_to_html(
        template_params, config.changelog_path)
    template_params["installInstructionsHtml"] = md_to_html(
        template_params, config.install_instructions_path)

    template = get_template("templates/index.html.jinja2")
    index = template.render(template_params)

    with open(f"{config.out_dir}/index.html", 'w', encoding="UTF-8") as indexfile:
        indexfile.write(index)

    copytree("style", f"{config.out_dir}/style")

    zip_out = f"{config.out_dir}/install-{config.device}.zip"
    boot_out = f"{config.out_dir}/boot-{config.device}.img"

    print("-- Copying installer and boot image")
    copyfile(config.zip, zip_out)
    copyfile(config.boot, boot_out)

    print("-- Generating SHA256 files")
    write_sha256(zip_out)
    write_sha256(boot_out)

    if not config.remove_vbmeta:
        print("-- Copying VBMeta and sha256sum")
        vbmeta_out = f"{config.out_dir}/vbmeta.img"
        copyfile("vbmeta.img", vbmeta_out)
        write_sha256(vbmeta_out)


if __name__ == "__main__":
    main()
