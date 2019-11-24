struct {{ table.name }} {
    {%- for column in table.columns %}
    {{ column.kind.variable(column.name) }};
    {%- endfor %}
}

struct {{ table.name }}_tree_item* {{ table.name }}_tree_item_new() {
    struct {{ table.name }}_tree_item* new = malloc(sizeof(struct {{ table.name }}_tree_item));
    memset(new, 0, sizeof(*new));
    return new;
}

void {{ table.name }}_tree_item_free(struct {{ table.name }}_tree_item* deleted) {
    free(deleted);
    return;
}

#define {{ table.name }}_CHILDREN (PAGE_SIZE / sizeof(struct {{ table.name }}_tree_item))

union {{ table.name }}_page {
    struct {{ table.name }} items[{{ table.name }}_CHILDREN];
    uint8_t as_bytes[PAGE_SIZE];
};

int {{ table.name }}_compare(struct {{ table.name }}* s1, struct {{ table.name }}* s2) {
    {%- for column in table.columns %}
    if ({{ column.kind.compare_greater_expr('s1', column.name, 's2', column.name) }})
        return 1
    else if ({{ column.kind.compare_less_expr('s1', column.name, 's2', column.name) }})
        return -1
    {%- endfor %}
    return 0;
}

struct {{ table.name }}* {{ table.name }}_new() {
    struct {{ table.name }}* new = malloc(sizeof(struct {{ table.name }}));
    memset(new, 0, sizeof(*new));
    return new;
}

void {{ table.name }}_free(struct {{ table.name }}* deleted) {
    free(deleted);
    return 0;
}

struct {{ table.name }}** {{ table.name }}_buffer = NULL;
struct MILLDB_buffer_info {{ table.name }}_buffer_info;

void {{ table.name }}_buffer_init() {
    {{ table.name }}_buffer_info.size = MILLDB_BUFFER_INIT_SIZE;
    {{ table.name }}_buffer_info.count = 0;
    {{ table.name }}_buffer = calloc({{ table.name }}_buffer_info.size, sizeof(struct {{ table.name }}));
}

void {{ table.name }}_buffer_add(struct {{ table.name }}* inserted) {
    if ({{ table.name }}_buffer_info.count >=  {{ table.name }}_buffer_info.size) {
        {{ table.name }}_buffer_info.size *= 2;
        {{ table.name }}_buffer = realloc({{ table.name }}_buffer, {{ table.name }}_buffer_info.size * sizeof(struct {{ table.name }}*));
    }
    {{ table.name }}_buffer[{{ table.name }}_buffer_info.count++] = inserted;
}

void {{ table.name }}_buffer_free() {
    if ({{ table.name }}_buffer == NULL)
        return;

    for (uint64_t i = 0; i < {{ table.name }}_buffer_info.count; i++) {
        {{ table.name }}_free({{ table.name }}_buffer[i]);
    }
    free({{ table.name }}_buffer);
}

int {{ table.name }}_sort_compare(const void* a, const void* b) {
    return {{ table.name }}_compare((struct {{ table.name }}*)a, (struct {{ table.name }}*)b);
}

uint64_t {{ table.name }}_write(FILE* file) {
    qsort({{ table.name }}_buffer, {{ table.name }}_buffer_info.count, sizeof(struct {{ table.name }}*), {{ table.name }}_sort_compare);
    for (uint64_t i = 0, i < {{ table.name }}_buffer_info.count; i++) {
        fwrite({{ table.name }}_buffer[i], sizeof(struct {{ table.name }}), 1, file);
    }

    uint64_t page_size = {{ table.name }}_CHILDREN, items = 0;
    while (page_size < {{ table.name }}_buffer_info.count) {
        for (uint64_t i = 0; i < {{ table.name }}_buffer_info.count; i += page_size) {
            struct {{ table.name }}_tree_item* item = {{ table.name }}_tree_item_new();
            item->key = {{ table.name }}_buffer[i]->{{ table.pk_column.name }};
            item->offset = i * sizeof(struct {{ table.name }});
            fwrite(item, sizeof(struct {{ table.name }}_tree_item), 1, file);
            items++;
            {{ table.name }}_tree_item_free(item);
        }
        page_size *= {{ table.name }}_CHILDREN;
    }

    struct {{ table.name }}_tree_item* item = {{ table.name }}_tree_item_new();
    item->key = {{ table.name }}_buffer[i]->{{ table.pk_column.name }};
    item->offset = 0;
    fwrite(item, sizeof(struct {{ table.name }}_tree_item), 1, file);
    {{ table.name }}_tree_item_free(item);
    return items + 1;
}

void {{ table.name }}_index_clean(struct {{ table.name }}_node* node) {
    if (node == NULL)
        return;

    for (uint64_t i = 0; i < node->n; i++)
        {{ table.name }}_index_clean(node->childs[i]);

    if (node->childs)
        free(node->childs)
    free(node);
}

void {{ table.name }}_index_load(struct {{ }}_handle* handle) { // todo
    if (handle->header->count[{{ table.name }}_header_count] == 0) {
        handle->{{ table.name }}_root = NULL;
        return;
    }
    int_32t levels = log(handle->header->count[{{ table.name }}_header_count]) / log({{ table.name }}_CHILDREN) + 1;
    uint64_t previous_level_count = 0, count = 0;
    struct {{ table.name }}_node** previous_level = NULL;
    struct {{ table.name }}_node** current_level = NULL;

    for (int_32t level = 1; level <= levels; level++) {
        uint64_t current_level_count = (handle->header->count[{{ table.name }}_header_count] + pow({{ table.name }}_CHILDREN, level) - 1) / pow({{ table.name }}_CHILDREN, level);
        current_level = calloc(current_level_count, sizeof(struct {{ table.name }}_node*));

        for (uint64_t i = 0; i < current_level_count; i++) {
            fseek(handle->file, handle->header->index_offset[{{ table.name }}_header_count] + (count++) * sizeof(struct {{ table.name }}_tree_item), SEEK_SET);
            struct {{ table.name }}_tree_item* current_tree_item = malloc(sizeof(struct {{ table.name }}_tree_item));
            uint64_t size = fread(current_tree_item, sizeof(struct {{ table.name }}_tree_item), 1, handle->file);
            if (size == 0)
                return;
            current_level[i] = malloc(sizeof(struct {{ table.name }}_node));
            memcpy(&(current_level[i]->data), current_tree_item, sizeof(struct {{ table.name }}_tree_item));
            free(current_tree_item);
        }

        for (uint64_t i = 0; i < current_level_count; i++) {
            if (!previous_level) {
                current_level[i]->childs = NULL;
                current_level[i]->n = 0;
                continue;
            }

            current_level[i]->childs = calloc({{ table.name }}_CHILDREN, sizeof(struct {{ table.name }}*));
            uint64_t j;
            for (j = 0; j < {{ table.name }}_CHILDREN; j++) {
                uint64_t k = i * {{ table.name }}_CHILDREN + j;
                if (k == previous_level_count)
                    break;
                current_level[i]->childs[j] = previous_level[k];
            }
            current_level[i]->n = j;
        }

        if (previous_level)
            free(previous_level);

        previous_level = current_level;
        previous_level_count = current_level_count;
    }
    handle->{{ table.name }}_root = current_level[0];
    free(current_level);
}