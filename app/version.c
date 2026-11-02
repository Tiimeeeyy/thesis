#include <stdio.h>
#include "ocgapi.h"

int main(void) {
    int major, minor;
    OCG_GetVersion(&major, &minor);
    printf("ocgcore API %d.%d\n", major, minor);
    return 0;
}
