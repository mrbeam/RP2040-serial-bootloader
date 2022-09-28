#ifndef BL_UTILS_H_INCLUDED
#define BL_UTILS_H_INCLUDED

#define STR_INDIR(x) #x 
#define STR(x) STR_INDIR(x)  
// WD_TO_MAX_MS macro is expanded into the value 8000 first from the STR macro, then passed to the STR_INDIR macro
// The call to the STR macro takes BL_WD_TO_MAX_MS macro as argument and passes the expanded value to the STR_INDIR macro 

#endif
