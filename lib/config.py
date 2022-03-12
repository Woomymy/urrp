# Web page configuration
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

    def __init__(self, 
        device: str,
        prettyname: str,
        boot: str = "",
        zip: str = "",
        remove_vbmeta: bool = False, 
        out_dir: str = "out",
        release: str = "1",
        is_orangefox: bool = False,
        maintainer: str = "Unknown",
        changelog_path: str = "",
        install_instructions_path: str = ""):
            self.device = device
            self.prettyname = prettyname
            self.boot = boot
            self.zip = zip
            self.remove_vbmeta = remove_vbmeta
            self.out_dir = out_dir
            self.release = release
            self.is_orangefox = is_orangefox
            self.maintainer = maintainer
            self.changelog_path = changelog_path
            self.install_instructions_path = install_instructions_path

def fix_home_path(path: str) -> str:
    """
    Fix ~ in paths, and replace them with $HOME
    """
    return path.replace("~", environ.get("HOME"))

def load_config() -> PageConfig:
    cli = ArgumentParser(
        description="recovery_rel_page cli",
        prog="recovery_rel_page"
    )

    cli.add_argument('--config', type=str, help="JSON configuration files", required=False, default="")

    args = cli.parse_args()
    configJson = "{}"
    # Check if config.json exists and load it
    if args.config != "":
        if exists(args.config):
            with open(args.config, 'r') as config:
                configJson = config.read()
    
    configObj = loadjson(configJson)
    return PageConfig(
        device=configObj["device"],
        prettyname=configObj["prettyname"],
        boot=fix_home_path(configObj["boot"]),
        zip=fix_home_path(configObj["zip"]),
        remove_vbmeta=configObj["remove_vbmeta"] if "remove_vbmeta" in configObj else False,
        out_dir=fix_home_path(configObj["out_dir"]) if "out_dir" in configObj else "out",
        release=configObj["release"] if "release" in configObj else "1",
        is_orangefox=configObj["is_orangefox"] if "is_orangefox" in configObj else False,
        maintainer=configObj["maintainer"],
        # Replace ~ with /home/USER
        changelog_path=fix_home_path(configObj["changelog"]),
        install_instructions_path=fix_home_path(configObj["install_instructions"])
    )
