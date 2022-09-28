#ifndef BL_CONFIG_H_INCLUDED
#define BL_CONFIG_H_INCLUDED

#include "bl_version.h"
#include "bl_utils.h"
#include "hardware/uart.h"

// WATCHDOG
#define BL_WD_TO_MAX_MS                     (8000)

// UART
#define UART_ID 	                        (uart0)
#define UART_TX_PIN                         0
#define UART_RX_PIN                         1
#define UART_BAUD                           (115200)
#define UART_WAIT_FOR_TRIGGER_TOUT_US       (1000000)

#define BL_IDENTIFIER_STR "BL" "##" VERSION_MAJOR "." VERSION_MINOR "." VERSION_PATCH "." VERSION_OTHERS "##" STR(BL_WD_TO_MAX_MS) "##"

#endif
