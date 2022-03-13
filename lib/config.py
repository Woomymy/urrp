"""
Utilities for loading configuration
"""

from argparse import ArgumentParser
from os import environ
from os.path import exists
from json import loads as loadjson


class PageConfig:
    """
    Web page configuration
    """

    device: str
    prettyname: str
    boot: str
    zip: str
    remove_vbmeta: bool = False
    out_dir: str = "out"
    release: str = "1"
    is_orangefox: bool = False
    maintainer: str = "Unknown"
    changelog_path: str
    install_instructions_path: str
    gpg_sign: bool
    gpg_cli_opts: str

    def __init__(self,
                 device: str,
                 prettyname: str,
                 boot: str = "",
                 zip_installer: str = "",
                 remove_vbmeta: bool = False,
                 out_dir: str = "out",
                 release: str = "1",
                 is_orangefox: bool = False,
                 maintainer: str = "Unknown",
                 changelog_path: str = "",
                 install_instructions_path: str = "",
                 gpg_sign: bool = False,
                 gpg_cli_opts: str = ""):
        self.device = device
        self.prettyname = prettyname
        self.boot = boot
        self.zip = zip_installer
        self.remove_vbmeta = remove_vbmeta
        self.out_dir = out_dir
        self.release = release
        self.is_orangefox = is_orangefox
        self.maintainer = maintainer
        self.changelog_path = changelog_path
        self.install_instructions_path = install_instructions_path
        self.gpg_sign = gpg_sign
        self.gpg_cli_opts = gpg_cli_opts


def fix_home_path(path: str) -> str:
    """
    Fix ~ in paths, and replace them with $HOME
    """
    return path.replace("~", environ.get("HOME"))


def load_config() -> PageConfig:
    """
    Find config .json file and return PageConfig from it
    """
    cli = ArgumentParser(
        description="recovery_rel_page cli",
        prog="recovery_rel_page"
    )

    cli.add_argument('--config', type=str,
                     help="JSON configuration files", required=False, default="")

    args = cli.parse_args()
    config_json = "{}"

    # Check if config.json exists and load it
    if args.config != "":
        if exists(args.config):
            with open(args.config, 'r', encoding="UTF-8") as config:
                config_json = config.read()

    config_obj = loadjson(config_json)
    return PageConfig(
        device=config_obj["device"],
        prettyname=config_obj["prettyname"],
        boot=fix_home_path(config_obj["boot"]),
        zip_installer=fix_home_path(config_obj["zip"]),
        remove_vbmeta=config_obj["remove_vbmeta"] if "remove_vbmeta" in config_obj else False,
        out_dir=fix_home_path(
            config_obj["out_dir"]) if "out_dir" in config_obj else "out",
        release=config_obj["release"] if "release" in config_obj else "1",
        is_orangefox=config_obj["is_orangefox"] if "is_orangefox" in config_obj else False,
        maintainer=config_obj["maintainer"],
        # Replace ~ with /home/USER
        changelog_path=fix_home_path(config_obj["changelog"]),
        install_instructions_path=fix_home_path(
            config_obj["install_instructions"],
        ),
        gpg_sign=config_obj["gpg_sign"] if "gpg_sign" in config_obj else False,
        gpg_cli_opts=config_obj["gpg_cli_opts"] if "gpg_cli_opts" in config_obj else ""
    )
