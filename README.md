## RP2040 Serial bootloader

|Field       |Description                |
|------------|---------------------------|
|Author      | Brian Starkey (github.com/usedbytes)|
|Function    | Bootloader for the custom embedded apps in Mr Beam.|
|Info        | Customized for use with Mr Beam II Dreamcut RP2040 shields.|

The serial bootloader is used to jump to the custom embedded app developed for the Pico boards. The usage is in the Mr Beam II Dreamcut devices RP2040 boards are used.

Using a serial bootloader enables updates for the embedded software to be applied during a software release.

The .uf2 file is flashed on the RP2040 shield using TC2030-MCP-NL or similar on the 6-pin pad. We have the option to flash the bootloader only or in case of production bootloader+app. 

The bootloader is used as a submoudle by the grblhal-rp2040 repo to facilitate creation of the bootloader+app combination.

Opening a serial terminal with PuTTy or minicom or any similar app with the corresponding Serial/UART module address will show an output of the bootloader identifier string like the one below.
```
BL##v0.1.1##(8000)##
```

Flashing is done using the serial-flash tool. https://github.com/mrbeam/RP2040-serial-flash-tool



### POINTS TO NOTE:
---
1.<b>bootloader.ld</b>

* FLASH(rx) : ORIGIN = 0x10000000, LENGTH = 32k //maintain the length as multiple of 4k.
* Make similar changes in the other .ld files and CMakeLists.txt file
    * combined.ld
    * standalone.ld

Refer the branch - https://github.com/usedbytes/rp2040-serial-bootloader/tree/bl32k and the changes.

-------------------------------------

2.<b> main.c</b>

IMAGE_HEADER_OFFSET should be the same as the FLASH LENGTH variable in the bootloader.ld file.
``` 
#define IMAGE_HEADER_OFFSET (32 * 1024) 
```
When using different baud rates make sure to recompile the 
GOlang serial flash tool available in the following repo. - https://github.com/mrbeam/RP2040-serial-flash-tool.

```
 #define UART_BAUD   (250000)
 ```

Best to keep the baudrate same across the tools to avoid updating the flash tool itself.

--------------------------------------
3.<b>CMakeLists.txt</b>

Changing the size of the FLASH LENGTH becomes necessary new libraries are added.When the preprocessor #define DEBUG is declared in the cmake compile options the stdio_usb library is added. Make the following change in CMakeLists.txt file.


```
target_link_libraries(bootloader
                      pico_stdlib
                      hardware_dma
                      hardware_flash
                      hardware_structs
                      hardware_resets
                      pico_stdio_usb //Add this line.
                      cmsis_core)
```

Compile with the following options on the terminal for DEBUG option.
```
mkdir Debug
cd Debug
cmake -DUSE_DEBUG=ON ..  
make -j8
```
For Release builds
```
mkdir build
cd build
cmake ..  
make -j8
```
---

### Compiled bootloader version

CMake invokes `tools/generate_version.py` to obtain the version from this repository (including when built as a submodule).
A clean tagged commit reports `v1.1.2`; later commits report e.g.
`v1.1.2+3.gabc1234`, and tracked local changes append `.dirty`.
Without matching tags, development builds report `v0.0.0+0.g<commit>`.
Alpha tags such as `v2.8.0a0` are also supported, including development
versions such as `v2.8.0a0+1.g8e9187f` and their `.dirty` forms.
Fetch tags with `git fetch origin --tags`; the parent submodule remains pinned.
Version metadata is checked on each build, and the generated header is rewritten only
when its contents change. The `BL##<version>##(<watchdog-ms>)##` format is preserved.

For a source archive without Git metadata, explicitly configure
`cmake -DBOOTLOADER_VERSION_OVERRIDE=v1.1.2 ..`.
Release builds should use a clean checkout at the chosen `vMAJOR.MINOR.PATCH` tag.
No release tags are created automatically.
