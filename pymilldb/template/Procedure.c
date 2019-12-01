{%- if procedure.mode == 'READ' %}
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

{%- endif %}
{%- for statement in procedure.statements.values() %}
statement.print_dependencies()

void {{ procedure.name }}_{{ loop.index }}(
{%- if procedure.mode == 'WRITE' -%}
    {{ statement.print_full_signature(procedure.name) }}
{%- elif procedure.mode == 'READ' -%}
    struct {{ procedure.name }}_out* iter
    {%- for param in procedure.parameters.values() -%}
        {%- if param.mode == 'IN' -%}
            , {{ param.signature() }}
        {%- endif -%}
    {%- endfor -%}
{%- endif -%}
) {
    statement.print(procedure.name)
}

{%- endfor %}
{%- if procedure.mode == 'READ' %}
void {{ procedure.name }}_init(struct {{ procedure.name }}_out* iter, struct {{ context.NAME }}_handle* handle
{%- for param in procedure.parameters.values() -%}
    {%- if param.mode == 'IN' -%}
        , param.signature()
    {%- endif -%}
{%- endfor %}
) {
    memset(iter, 0, sizeof(*iter));
    iter->service.handle = handle;
    iter->service.set = NULL;
    iter->service.size = 0;
    iter->service.count = 0;
    iter->service.length = 0;

    {{ procedure.name }}_1(iter
    {%- for param in procedure.parameters.values() -%}
        {%- if param.mode == 'IN' -%}
            , param.name
        {%- endif -%}
    {%- endfor -%}
    );
}

int {{ procedure.name }}_next(struct {{ procedure.name }}_out* iter) {
    if (iter == NULL)
        return 0;

    struct {{ procedure.name }}_out_service* service = &(iter->service);

    if (service->set != NULL && service->count < service->length) {
        memcpy(&iter->data, &(service->set[service->count]), sizeof(struct {{ procedure.name }}_out_data));
        service->count++;
        return 1;
    } else {
        free(service->set);
    }
    return 0;
}

{%- endif %}
{%- if procedure.mode == 'WRITE' %}
void {{ procedure.name }} ({{ procedure.parameters | map(attribute='signature') | join(', ') }}) {
    {%- for statement in procedure.statements.values() %}
    {{ procedure.name }}_{{ loop.index }}({{ statement.print_argument }});
    {%- endfor %}
}

{%- endif %}