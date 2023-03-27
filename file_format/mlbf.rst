======================================
MLBF(Markup Language for Binary File)
======================================

version: 0.4.0; By Benjamin Fang

**A method/language to describe binary file orgnization**.

Introduction
++++++++++++++++++

I need a method to describe the layout of binary file quickly. So I presented this
method to do this.

For example, if you want to describe a binary organized as: :code:`"int(value is 222) int char(repeat 3 times) int(value is a) float(repeat a times)"`.

You can reprent it by:

.. code::

    [1]<int; =222>()
    [1]<int>(dsp="foo")
    [3]<char>(dsp="bar")
    [1]<int; $var>()
    [$var]<float>()


Syntax
++++++++++++++++++

.. code-block::

    [a_number | expression; @individual_name]
    <block_type | condition_expression; $variable_represent_value_of_this_block;>
    (lable="";)
    
    {...}


reserved characters:

1. key words

    key wrods of MLBF all begined with `%`

    .. code-block::

        %let
            define a varible and assign value
            example:
                [%let]<$a = 3>(dsp="assign value 3 to $a")

        %file
            refer a varible to a file
            example:
                [%file]<$f>(file="a file")

        %extern
            declear a varible which value is offer by user
            example:
            [%extern]<%ex>()

        %define

        %deflable

        %if %elif %else

        %for

        %while


2. data type

    (1) general varible

    (2) array    


3. standard lable

    id

    dsp

    file

    name

    value

4. lamda function

    $value($a, $b){$value = $a + $b; %for($i = 0; $i < 10; %i++){$value += $i}}

:code:`%let declear a varible and`

:code:`[], <>, (), {}`

:code:`$, @, %, # ~`

Detials
+++++++++++++++++++++++

1. [...] 

    The number of block. (NB)

    "..." can be:

    1. a number, which represent the number of block. For example :code:`[3]<int>(name="foo")`.

    2. expressions, consists constants and variables, the value of expression reprent the number of block. For example :code:`[$var_a * 2 + 3]<int>(name="foo")`

    3. a iterator, which start with "@", This is used to reprent the iteration of number of block. Example :code:`[76; @iterater_var_a]<int>(name="foo")`. Most of time, string after of :code:`@` can be omited, :code:`[$var_a; @]<int>()`, can use :code:`@var_a` to reference this iterator.  

    Each part is sperated by ";". Example :code:`[$var_a * 2; @ind_a]<int>(name="foo")`


2. <...>

    block type. (BT)

    "..." can be:

    1. a block type. Anyone of :code:`bit, byte, char, uint8, int, long, int32, uint32, uint64, float, double` and so on. Example :code:`[7]<int32>(name="foo")`.

    2. a variable begain with :code:`$`. For example :code:`[3]<long; $var_a>(name="foo")`. if NB is one, than :code:`$var` is a single value, else, :code:`$var` is a array of block values. 

    3. expressions, the value of expression will be assiigned to block. Example :code:`[3]<int; $var_a; $var_a = [31, 30, 29]>`, mean that value of this 3 blocks is 31, 30 and 29.

    Each part is sperated by ";".

3. (...)

    Attributes lables. (AL) 

    "..." are several :code:`lable="value"` attributes, sperated by ";".

4. {...}

    Block group. (BG)

    "{}" is used to group block which have more complex structure. Example :code:`[3]{[2]<int>() [1]<float>()}()`


5. Define lable

    Example:

    :code:`<>[](%deflable dsp "description")`

    This would define dsp lable. you can use a not defined lable, Define the lable when you want.

6. Globle lable

    Example:

    :code:`<>[](endianness="little")`

    This lable mean all multiple bytes integer is store by little endianness.

7. Comments

    :code:`[]<>(#this is a comment)`

    .. code::

        []<>(#--)
            all content within this is commented
        []<>(--#)


All characters between "[]", "<>", "()" and "{}" is ogmited.


Example
++++++++++++++++++

.. code-block::

    []<>(#besd sparse binary file)
    []<>(%deflable dsp "description of block")
    []<>(%deflable esi_index "index of esi snp/variant")
    []<>(endianness="little")
    [1]<int32>(dsp="besd type"; value="3 for SMR_SPARSE_3 SPARSE_BELT sparse format")  
    [1]<int32>(dsp="sample size", value="-9 for NA";)  
    [1]<int32; $esi_num>(dsp="esi number")  
    [1]<int32; $epi_num>(dsp="epi number")  
    [12]<int32>(value="-9")  
    [1]<uint64; $value_num; $value_num = 0; for(i = 1; i < $epi_num; i++){$value_num += @epi_num.$beta_offset + @epi_num.$se_offset}>(dsp="number of sparse beta and se value")  
    [1]<uint64>(value="0")
    [$epi_num; @]{  
        [1]<uint64; @epi_num.$beta_offset>(dsp="number of esi offset")
        [1]<uint64; @epi_num.$se_offset>(dsp="number of esi offset") 
    }(dsp="beta and se offsets number of each probe"; order="same as epi file")
    [$epi_num; @]{
        [@epi_num.$beta_offset; @]<uint32; $beta_index>(dsp="beta index of esi", order="esi file")
        [@epi_num.$se_offset; @]<uint32; $se_index>(dsp="se index of esi", order="esi file")
    }(dsp="beta and se esi index arrary of each probe", order="same as epi file")
    [$epi_num; @]{
        [@epi_num.$beta_offset]<float>(dsp="esi beta value"; esi_index=$beta_index)
        [@epi_num.$se_offset]<float>(dsp="esi se value"; esi_index=$se_index)
    }(dsp="beta as se value", order="epi file")

Here are more example within this directory.
