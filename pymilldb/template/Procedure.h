{%- if procedure.mode == 'READ' %}
struct {{ procedure.name }}_out_data {
    {%- for param in procedure.parameters %}
    {%- if param.mode == 'OUT' %}
    {{ param.kind.str_out(param.name) }};
    {%- endif %}
    {%- endfor %}
};

struct {{ procedure.name }}_out_service {
    struct {{ }}_handle* handle; // todo
    struct {{ procedure.name }}_out_data* set;
    int size;
    int length;
    int count;
};

struct {{ procedure.name }}_out {
    struct {{ procedure.name }}_out_service service;
    struct {{ procedure.name }}_out_data data;
};

{%- endif %}
{%- if procedure.mode == 'READ' %}
void {{ procedure.name }}_init(struct {{ procedure.name }}_out* iter, struct {{ }}_handle* handle  // todo
{%- for param in procedure.parameters -%}
    {%- if param.mode == 'IN' -%}
        , param.signature()
    {%- endif -%}
{%- endfor %}
);

int {{ procedure.name }}_next(struct {{ procedure.name }}_out* iter);

{%- endif %}
{%- if procedure.mode == 'WRITE' %}
void {{ procedure.name }} ({{ procedure.parameters | map(attribute='signature') | join(', ') }});

{%- endif %}