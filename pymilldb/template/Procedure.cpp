struct {{ procedure.name }}_out_data {
    {%- for param in procedure.parameters }
    {%- if param.mode == 'OUT' }
    {{ param.kind.str_out(param.name) }};
    {%- endif %}
    {%- endfor %}
};

struct {{ procedure.name }}_out_service {
    struct {{ }}_handle* handle;
    struct {{ procedure.name }}_out_data* set;
    int size;
    int length;
    int count;
};

struct {{ procedure.name }}_out {
    struct {{ procedure.name }}_out_service service;
    struct {{ procedure.name }}_out_data data;
};

void {{ procedure.name }}_add(struct {{ procedure.name }}_out* iter, struct {{ procedure.name }}_out_data* selected) {
    struct {{ procedure.name }}_out_service* service = &(iter->service);
    if (service->set == NULL) {
        service->size = MILLDB_BUFFER_INIT_SIZE;
        service->set = calloc(service->size, sizeof(struct {{ procedure.name }}_out));
    }
    if (service->length >= service->size) {
        service->size = service->size * 2;
        service->set = realloc(service->set, service->size * sizeof(struct {{ procedure.name }}_out));
    }
    memcpy(&(service->set[service->length++]), selected, sizeof(struct {{ procedure.name }}_out_data));
}


