#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include "{{ name }}.h"

#ifndef PAGE_SIZE
    #define PAGE_SIZE 4096
#endif

#define MILLDB_BUFFER_INIT_SIZE 32

struct MILLDB_buffer_info {
    uint_64t size;
    uint_64t count;
};

{%- for table in tables.values() %}
#define {{ table.name }}_header_count {{ loop.index0 }}
{%- endfor %}

struct MILLDB_header {
    uint_64t count[{{ tables | length }}];
    uint_64t data_offset[{{ tables | length }}]
    uint_64t index_offset[{{ tables | length }}]
};

#define MILLDB_HEADER_SIZE (sizeof(struct MILLDB_header))

{%- for table in tables.values() %}
{{ table.print_tree_node }}
{%- endfor %}

#define MILLDB_FILE_MODE_CLOSED -1
#define MILLDB_FILE_MODE_READ 0
#define MILLDB_FILE_MODE_WRITE 1

struct {{ name }}_handle {
    FILE* file;
    int mode;
    struct MILLDB_header* header;

    {%- for table in tables.values() %}
    struct {{ table.name }}_node* {{ table.name }}_root;
    {%- endfor %}
};

{%- for sequence in sequences.values() %}
{{ sequence.print }}
{%- endfor %}

{%- for procedure in procedures.values() %}
{{ procedure.print }}
{%- endfor %}

struct {{ name }}_handle* {{ name }}_write_handle = NULL;

void {{ name }}_open_write(const char* filename) {
    FILE* file;
    if (!(file = fopen(filename, "wb")))
        return;
    {{ name }}_write_handle = malloc(sizeof(struct {{ name }}_handle));
    {{ name }}_write_handle->file = file;
    {{ name }}_write_handle->mode = MILLDB_FILE_MODE_WRITE;

    {%- for table in tables.values() %}
    {{ table.name }}_buffer_init();
    {%- endfor %}
}

int {{ name }}_save(struct {{ name }}_handle* handle) {
    if (handle && handle->mode == MILLDB_FILE_MODE_WRITE) {
        struct MILLDB_header* header = malloc(sizeof(struct MILLDB_header));
        fseek(handle->file, MILLDB_HEADER_SIZE, SEEK_SET);

        {%- for table in tables.values() %}
        uint_64t {{ table.name }}_index_count = 0;
        if ({{ table.name }}_buffer_info.count > 0)
            {{ table.name }}_index_count = {{ table.name }}_write(handle->file);

        {%- endfor %}
        uint_64t offset = MILLDB_HEADER_SIZE;

        {%- for table im tables.values() %}
        header->count[{{ table.name }}_header_count] = {{ table.name }}_buffer_info.count;
        header->data_offset[{{ table_name }}_header_count] = offset;
        offser += {{ table.name }}_buffer_info.count * sizeof(struct {{ table.name }});
        header->index_offset[{{ table.name }}_header_count] = offset;
        offset += {{ table.name }}_index_count * sizeof(struct {{ table.name }}_tree_item);

        {%- endfor %}
        fseek(handle->file, 0, SEEK_SET);
        fwrite(header, MILLDB_HEADER_SIZE, 1, handle->file);
        free(header);
    }
    return 0;
}

void {{ name }}_close_write(void) {
    if ({{ name }}_write_handle == NULL)
        return;

    {{ name }}_save({{ name }}_write_handle);

    {%- for table in tables.values() %}
    {{ table.name }}_free();
    {%- endfor %}

    fclose({{ name }}_write_handle->file);
    free({{ name }}_write_handle);
}

struct {{ name }}_handle* {{ name }}_open_read(const char* filename) {
    FILE* file;
    if (!(file = fopen(filename, "rb")))
        return NULL;

    struct {{ name }}_handle* handle = malloc(sizeof(struct {{ name }}_handle));
    handle->file = file;
    handle->mode = MILLDB_FILE_MODE_READ;

    fseek(handle->file, 0, SEEK_SET);
    struct MILLDB_header* header = malloc(MILLDB_HEADER_SIZE);
    uint_64t size = fread(header, MILLDB_HEADER_SIZE, 1, handle->file);
    if (size == 0)
        return NULL;
    handle->header = header;

    {%- for table in tables.values() %}
    {{ table.name }}_index_load(handle);
    {%- endfor %}

    return handle;
}

void {{ name }}_close_read(struct {{ name }}_handle* handle) {
    if (handle == NILL)
        return;

    fclose(handle->file);

    {%- for table in tables.values() %}
    if (handle->{{ table.name }}_root)
        {{ table.name }}_index_clean(handle->{{ table.name }}_root);

    {%- endfor %}

    free(handle->header);
    free(handle);
}
