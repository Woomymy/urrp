#### Without TWRP

> _Note: You need a copy of your ROM boot.img_

> _This device **DOES NOT** support `fastboot boot twrp.img`_

1. Reboot your phone into fastboot mode
2. Download Blank VBmeta and flash it using `fastboot flash vbmeta vbmeta.img`
3. Next, download TWRP **.IMG** file and flash it using `fastboot flash boot IMAGE_NAME.img`
4. Reboot into recovery mode (`fastboot reboot recovery`)
5. When booted into recovery, reflash stock boot.img (Install -> Install Image -> Select stock boot.img -> "Flash to: Boot")
6. Next, go in Advanced -> Flash current TWRP and swipe to flash TWRP.
7. Reboot and enjoy!

#### With TWRP/OrangeFox

1. Download TWRP/OrangeFox **.ZIP** installer and flash it with TWRP
