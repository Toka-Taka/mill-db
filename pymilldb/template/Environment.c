#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include "{{ context.NAME }}.h"

#ifndef PAGE_SIZE
    #define PAGE_SIZE 4096
#endif

#define MILLDB_BUFFER_INIT_SIZE 32

struct MILLDB_buffer_info {
    uint64_t size;
    uint64_t count;
};
{% for table in context.TABLES.values() %}
#define {{ table.name }}_header_count {{ loop.index0 }}
{%- endfor %}

struct MILLDB_header {
    uint64_t count[{{ context.TABLES | length }}];
    uint64_t data_offset[{{ context.TABLES | length }}];
    uint64_t index_offset[{{ context.TABLES | length }}];
};

#define MILLDB_HEADER_SIZE (sizeof(struct MILLDB_header))

{%- for table in context.TABLES.values() %}

struct {{ table.name }}_tree_item {
    {{ table.pk_column.kind.variable('key') }};
    uint64_t offset;
};

struct {{ table.name }}_node {
    struct {{ table.name }}_tree_item data;
    struct {{ table.name }}_node** childs;
    uint64_t n;
};
{%- endfor %}

#define MILLDB_FILE_MODE_CLOSED -1
#define MILLDB_FILE_MODE_READ 0
#define MILLDB_FILE_MODE_WRITE 1

struct {{ context.NAME }}_handle {
    FILE* file;
    int mode;
    struct MILLDB_header* header;
    {% for table in context.TABLES.values() %}
    struct {{ table.name }}_node* {{ table.name }}_root;
    {%- endfor %}
};

{%- for table in context.TABLES.values() %}

{% include 'Table.c' -%}
{%- endfor %}

{%- for procedure in context.PROCEDURES.values() %}

    {%- if procedure.is_write %}
        {%- include 'ProcedureWrite.c' %}
    {%- elif procedure.is_read %}
        {%- include 'ProcedureRead.c' %}
    {%- endif %}
{% endfor %}

struct {{ context.NAME }}_handle* {{ context.NAME }}_write_handle = NULL;

void {{ context.NAME }}_open_write(const char* filename) {
    FILE* file;
    if (!(file = fopen(filename, "wb")))
        return;
    {{ context.NAME }}_write_handle = malloc(sizeof(struct {{ context.NAME }}_handle));
    {{ context.NAME }}_write_handle->file = file;
    {{ context.NAME }}_write_handle->mode = MILLDB_FILE_MODE_WRITE;

    {%- for table in context.TABLES.values() %}
    {{ table.name }}_buffer_init();
    {%- endfor %}
}

int {{ context.NAME }}_save(struct {{ context.NAME }}_handle* handle) {
    if (handle && handle->mode == MILLDB_FILE_MODE_WRITE) {
        struct MILLDB_header* header = malloc(sizeof(struct MILLDB_header));
        fseek(handle->file, MILLDB_HEADER_SIZE, SEEK_SET);

        {%- for table in context.TABLES.values() %}
        uint_64t {{ table.name }}_index_count = 0;
        if ({{ table.name }}_buffer_info.count > 0)
            {{ table.name }}_index_count = {{ table.name }}_write(handle->file);

        {%- endfor %}
        uint_64t offset = MILLDB_HEADER_SIZE;

        {%- for table in context.TABLES.values() %}
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

void {{ context.NAME }}_close_write(void) {
    if ({{ context.NAME }}_write_handle == NULL)
        return;

    {{ context.NAME }}_save({{ context.NAME }}_write_handle);

    {%- for table in context.TABLES.values() %}
    {{ table.name }}_free();
    {%- endfor %}

    fclose({{ context.NAME }}_write_handle->file);
    free({{ context.NAME }}_write_handle);
}

struct {{ context.NAME }}_handle* {{ context.NAME }}_open_read(const char* filename) {
    FILE* file;
    if (!(file = fopen(filename, "rb")))
        return NULL;

    struct {{ context.NAME }}_handle* handle = malloc(sizeof(struct {{ context.NAME }}_handle));
    handle->file = file;
    handle->mode = MILLDB_FILE_MODE_READ;

    fseek(handle->file, 0, SEEK_SET);
    struct MILLDB_header* header = malloc(MILLDB_HEADER_SIZE);
    uint_64t size = fread(header, MILLDB_HEADER_SIZE, 1, handle->file);
    if (size == 0)
        return NULL;
    handle->header = header;

    {%- for table in context.TABLES.values() %}
    {{ table.name }}_index_load(handle);
    {%- endfor %}

    return handle;
}

void {{ context.NAME }}_close_read(struct {{ context.NAME }}_handle* handle) {
    if (handle == NILL)
        return;

    fclose(handle->file);

    {%- for table in context.TABLES.values() %}
    if (handle->{{ table.name }}_root)
        {{ table.name }}_index_clean(handle->{{ table.name }}_root);

    {%- endfor %}

    free(handle->header);
    free(handle);
}
