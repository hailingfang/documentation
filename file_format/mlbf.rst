==========
MLBF(Markup Language for Binary File)
==========

A method/language to describe binary file orgnization.
==========================================================

Introduction
++++++++++++++++++

I need a method to describe the layout of binary file quickly. So I presented this
method to do this.

Syntax
++++++++++++++++++

.. code-block::

    [a_number; expression; @individual_name]
    <block_type; $variable_value_assignedto; |expression>
    (lable="";)
    {...}


Above is syntax of language. the [], <>, (), {} is conserved as key as syntex.


1. [...] 

    The repeat of unit.

    "..."
    
    can be a number which reprent have repeat times;(required)

    can  be a expression, the value of expression reprent the repeat times;

    can be a symble which start with "@", this same is name of individual. 

    each part is sperated by ";".

2. <...>

    Unit type.

    "..."

    can be a unit type, include: bit, byte, char, int, long, uint32, float et al;(required)

    can be a symble which start with "$", this symble is variable reprent the value of the unit;

    can be a expression start with "|", the value of expression will be assiigned to unit;

    each part is sperated by ";".

3. (...)

    Atributes.

    "..."

    is saveral 'lable=""' part which sperated by ";".

4. {...}

    "[...]<...>(...)" make up a block.
    
    "{}" is used to group them. It can have "[]" at start or have a "()" at end.

All characters between "[]", "<>", "()" and "{}" is ogmited.

Example
++++++++++++++++++

.. code-block::

    #Example:

    [1]<uint32>(value="1, 2 ,3"; describe="head flag")
    [1]<uint32; $var1>(describe="head size")
    [$var1 + 2]<char>()
    [12]{
        [3]<uint64>()
        [1]<float32>()
    }()
    [1]{
        [2]<bit>()
        [2]<bit>()
        [1]<bit>()
        [3]<bit|$flag>()

    }()
    [$flag > 0? 1: 0]<int32>()
    [1]<int =$var1 * 10>()


Here are more example within this directory.
