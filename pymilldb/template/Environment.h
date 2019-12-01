#ifndef {{ name | upper }}_H
#define {{ name | upper }}_H

#include <stdint.h>

#define MAX(x, y) (((x) > (y))? (x) : (y))
#define MIN(x, y) (((x) < (y))? (x) : (y))

#define {{ name }}_handle;

// todo sequence? procedure?

void {{ name }}_open_write(const char* filename);
void {{ name }}_close_write(void);

struct {{ name }}_handle* {{ name }}_open_read(const char* filename);
void {{ name }}_close_read(struct {{ name }}_handle* handle);

#endif