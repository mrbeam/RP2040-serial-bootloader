## RP2040 Serial bootloader

|Field       |Description                |
|------------|---------------------------|
|Author      | Brian Starkey (github.com/usedbytes)|
|Function    | Bootloader for the custom embedded apps in Mr Beam.|
|Info        | Customized for use with Mr Beam 3 Pico boards.|
|This version| v0.1.1                    |
|Date        | 2022-09-11                |

The serial bootloader is used to jump to the custom embedded app developed for the Pico boards. The usage is in the Mr Beam 3 devices where two RPi RP2040 Pico boards are used.

Using a serial bootloader enables updates for the embedded software to be applied during a software release.

The .uf2 file is copied and pasted on the RPi Pico during initial configuration. 

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
 #define UART_BAUD   (115200)
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
