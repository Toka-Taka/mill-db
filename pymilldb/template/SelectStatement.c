
void {{ procedure.name }}_{{ loop.index }}(
    struct {{ procedure.name }}_out* iter
    {%- set comma = joiner(', ') -%}
    {%- for param in procedure.parameters.values() -%}
        {%- if param.is_input -%}
            {{ comma() }}{{ param.signature }}
        {%- endif -%}
    {%- endfor -%}
) {
    {%- for table_data in statement.tables.values() %}
    {%- set table = table_data['table'] %}
    {%- for cond in table_data['conditions'] %}
    /* table {{ table.name }}    cond: {{ cond.print }} */
    {%- endfor %}
    {%- endfor %}
    struct {{ context.NAME }}_handle* handle = iter->service.handle;
    struct {{ procedure.name }}_out_data* inserted = malloc(sizeof(struct {{ procedure.name }}_out_data));
    {%- for table_data in statement.tables.values() %}
    {%- set table = table_data['table'] %}
    /* TABLE {{ table.name }} */
    {%- endfor %}
}
