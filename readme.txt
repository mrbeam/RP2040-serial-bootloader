POINTS TO NOTE:

* bootloader.ld

-> FLASH(rx) : ORIGIN = 0x10000000, LENGTH = 32k //maintain the length as multiple of 4k
-> Make similar changes in the other .ld files and CMakeLists.txt file
    combined.ld
    standalone.ld

Refer the branch - https://github.com/usedbytes/rp2040-serial-bootloader/tree/bl32k and the changes.

-------------------------------------

* main.c

-> #define IMAGE_HEADER_OFFSET (32 * 1024) //Should be the same as the FLASH LENGTH
variable in the bootloader.ld file

-> #define UART_BAUD   (115200) //when using different baud rates make sure to recompile the 
GOlang serial flash tool available in the following repo. - https://github.com/mrbeam/RP2040-serial-flash-tool
Best to keep the baudrate same across the tools to avoid updating the flash tool itself

--------------------------------------

Changing the size of the FLASH LENGTH becomes necessary when uisng #define DEBUG in the main.c
If #define DEBUG is used in main.c, make the following change in CMakeLists.txt file.

* CMakeLists.txt

-> target_link_libraries(bootloader
                      pico_stdlib
                      hardware_dma
                      hardware_flash
                      hardware_structs
                      hardware_resets
                      pico_stdio_usb
                      cmsis_core)