{%- for statement in procedure.statements %}
{% include 'InsertStatement.c' %}
{%- endfor %}

void {{ procedure.name }}(
    {%- set comma = joiner(', ') -%}
    {%- for param in procedure.parameters.values() -%}
        {%- if param.signature -%}
            {{ comma() }}{{ param.signature }}
        {%- endif -%}
    {%- endfor -%}
) {
    {%- for statement in procedure.statements %}
    {{ procedure.name }}_{{ loop.index }}(
        {%- set comma = joiner(', ') -%}
        {%- for arg in statement.arguments -%}
            {%- if arg.print -%}
                {{ comma() }}{{ arg.print }}
            {%- endif -%}
        {%- endfor -%}
    );
    {%- endfor %}
}
