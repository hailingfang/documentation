Jinja2 Syntax Notes
==========================


1. Variables
---------------------

.. code::

    {{ EXPRESSION }}


2. Conditionals
---------------------

.. code::

    {% if EXPRESSION %}
        ...
    {% elif EXPRESSION %}
        ...
    {% else %}
        ...
    {% endif %}


3. Loops
--------------------

.. code::

    {% for item in items %}
        ...{{ item }}...
    {% endfor %}
    
    Loop special variables:

    {{ loop.index }}        {# 1-based #}
    {{ loop.index0 }}       {# 0-based #}
    {{ loop.first }}
    {{ loop.last }}


4. Template Inheritance
-------------------------------

.. code::

    {% block block_name %}{% endblock %}

    {% extends "extended_template_name" %}


.. code::
    
    #Example:

    #layout.html
    <!DOCTYPE html>
    <html>
    <body>
      <h1>Site Header</h1>
      {% block content %}{% endblock %}
    </body>
    </html>
    
    #webpage.thml
    {% extends "layout.html" %}

    {% block content %}
      <p>This is the page content.</p>
    {% endblock %}


5. Including Templates
----------------------------

.. code::

    {% include "included_file_name.html" %}



6. Macros
------------------

.. code::

    {% macro button(text, type="primary") %}
      <button class="{{ type }}">{{ text }}</button>
    {% endmacro %}

    {{ button("Save") }}
    {{ button("Delete", "danger") }}


7. Importing Macros
--------------------------

.. code::

    {% import "macros.html" as ui %}
    {{ ui.button("Click me") }}


8. Filters
------------------

.. code::
 
    {{ name | upper }}
    {{ text | replace("old", "new") }}
    {{ items | length }}
    {{ content | safe }}    {# do not escape HTML #}
    
    Common filters:
    upper, lower
    title
    length
    replace("a","b")
    join(", ")
    safe (disable autoescape)
    default("value")

.. image:: ./jinja2-syntax/jinja2-builtin-filters.png
   :width: 98%


9. Set Variables in Template
-------------------------------------

.. code::

    {% set total = price * quantity %}
    <p>Total: {{ total }}</p>


10. Raw Blocks
---------------------

.. code::

    {% raw %}
    {{ this_will_not_be_rendered }}
    {% endraw %}


11. Comments
------------------------------

.. code::

    {# This is a comment and will not appear in output #}



---------------------------------------------------

References
-------------------

https://jinja.palletsprojects.com/en/stable/templates/
