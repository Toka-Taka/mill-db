
void {{ procedure.name }}_{{ loop.index }}(
    {%- set comma = joiner(', ') -%}
    {%- for arg in statement.arguments -%}
        {%- if arg.signature %}{{ comma() }}{{ arg.signature }}{%- endif -%}
    {%- endfor -%}
) {
    struct {{ statement.table.name }}* inserted = {{ statement.table.name }}_new();
    {%- for col, arg in zip(statement.table.columns.values(), statement.arguments) %}
    {%- if isinstance(col.kind, context.Char) %}
    memcpy(inserted->{{ col.name }}, {{ arg.name }}, {{ col.kind.size }});
    {%- else %}
    inserted->{{ col.name }} =
        {%- if isinstance(arg, context.ArgumentSequenceCurrent) -%}
            {{' ' ~ arg.name }}
        {%- elif isinstance(arg, context.ArgumentSequenceNext) -%}
            {{' ++' ~ arg.name }}
        {%- elif isinstance(arg, context.ArgumentParameter) -%}
            {{' ' ~ arg.name }}
        {%- endif %};
    {%- endif %}
    {%- endfor %}
    {{ statement.table.name }}_buffer_add(inserted);
}
