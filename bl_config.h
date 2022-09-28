#ifndef BL_CONFIG_H_INCLUDED
#define BL_CONFIG_H_INCLUDED

#include "bl_version.h"
#include "bl_utils.h"

#define BL_IDENTIFIER_STR "BL" "##" VERSION_MAJOR "." VERSION_MINOR "." VERSION_PATCH "." VERSION_OTHERS "##" STR(BL_WD_TO_MAX_MS) "##"

#endif
