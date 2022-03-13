# TWRP/Ofox releases page

Simple release page for Unofficial TWRP/OrangeFox builds

## Dependencies

- pandoc (to convert markdown to HTML)

## Usage

`python template.py --config /path/to/config_file.json`

### Configuration

The configuration should be stored in a JSON file.

Example configuration:

```json
{
  "device": "rosemary", // Device codename
  "prettyname": "Redmi Note 10S", // Device name
  "boot": "~/TWRP/boot-rosemary.img", // Path to boot.img
  "zip": "~/TWRP/installer-rosemary.zip", // Path to installer ZIP
  "remove_vbmeta": false, // Set to true to remove blank vbmeta.img
  "release": "3.6.1-11_1", // Release version
  "is_orangefox": true, // Set to true if the recovery is OrangeFox (default: False)
  "maintainer": "Woomymy", // Maintainer name
  "changelog": "changelog.md", // Path to changelog markdown file
  "install_instructions": "install.md" // Path to installation instructions
}
```

### Changelog/Install instructions

Changelog and installation instruction markdown files can also use jinja2 templating

#### List of variables aviable in changelog/install instructions

- recovery: Recovery name (TWRP or OrangeFox)
- marketname: Device name
- device: Device codename
- maintainer: Maintainer name
- version: Release version
- Include_vbmeta: true if blank vbmeta is included
- zip_name: Output zip name
- img_name: Output img name
- gpg_signed: True if files are signed with gpg

### Credits

Font used in page is [Iosevka](https://github.com/be5invis/Iosevka) is licensed under the SIL Open Font License 1.1. See [LICENSE_IOSEVKA file](./LICENSE_IOSEVKA) for more informations

### License

This project is licensed under the [MIT LICENSE, see LICENSE file for more details](./LICENSE)
