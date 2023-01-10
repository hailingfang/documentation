======================================
MLBF(Markup Language for Binary File)
======================================

version: 0.2; By Benjamin Fang

**A method/language to describe binary file orgnization**.

Introduction
++++++++++++++++++

I need a method to describe the layout of binary file quickly. So I presented this
method to do this.

Syntax
++++++++++++++++++

.. code-block::

    [a_number | expression; @individual_name]
    <block_type | condition_expression; $variable_represent_value_of_this_block;>
    (lable="";)
    {...}


Above is syntax of language. the :code:`[], <>, (), {}` is conserved as key as syntex. Those key make up
:code:`[...]<...>(...)` or :code:`[...]{...}(...)`. The :code:`[]` and :code:`()` of second combination can be omited.


1. [...] 

    The number of block.

    "..." can be:

    1. a number which represent the number of block. For example :code:`[3]<int>(name="foo")`.

    2. a expression consists constants and variables, the value of expression reprent the number of block. For example :code:`[$var_a * 2 + 3]<int>(name="foo")`

    3. a symble which start with "@", This is used to reprent the each block. Example :code:`[$var_a; @each_block]<int>(name="foo")` 

    Each part is sperated by ";". Example :code:`[$var_a * 2; @ind_a]<int>(name="foo")`


2. <...>

    block type.

    "..." can be:

    1. a block type. Anyone of :code:`bit, byte, char, uint8, int, long, int32, uint32, uint64, float, double` and so on. Example :code:`[7]<int32>(name="foo")`.

    2. a variable begain with '$'. For example :code:`[3]<long; $var_a>(name="foo")`.

    3. a expression start with :code:`|`, the value of expression will be assiigned to block. Example :code:`<int; |31>`.

    Each part is sperated by ";".

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
