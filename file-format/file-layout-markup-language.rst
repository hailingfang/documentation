============================================
Reference of File Layout Markup Language 
============================================

version: 1.0.0; by Benjamin Fang

creat: 20230401; update: 20230606

I need a method to describe the layout or format of a file.
Describing the format of a plaintext file is easy, you just need to
specify the meaning of every field. However, describing the layout of a binary
file can be difficult to do effectively and accurately. That's why I
developed this method.

This mothod is simple, and For example,
if you want to describe a binary organized 
as::

    3 integers, 1 char, which value is 255, 1 integer which have a value "X", "X" floats.

You can describe the layout using FLML like following::

    [3] <int> ()
    [1] <char; =255> ()
    [1] <int; :$x> (dsp="here assigned the vaule of this integer block to variable $x")
    [$x] <float> ()


Syntax
========================

FLML description is made of :code:`flml-sentence`, which is looks like
:code:`[block-number]<block-unit>(description)` or :code:`[block-number]{flml-sentence}(description)`.
spaces between :code:`file-sentence` will be ignored.

Using a modified BNF grammar notation. Which can be defined as::

    flml-syntax   ::= flml-sentence +
    file-sentence ::= "[" number-block "]" ( "<" uint-block ">" | "{" flml-sentence "}" ) "(" descriptions ")"


number-block
-----------------------

:code:`block-number` is mainlly used to describe the number of :code:`uint-block`.
:code:`block-number` can be a :code:`number`, :code:`variable`, or a :code:`expression`.

For example::

    [%let $n = 5]<>(dsp="assign 5 to $n")
    [3 * $n] <float> (dsp="this have 10 float")

:code:`block-number` can also have a interation variable.

For example::

    [5; ~$i]{
        [$i + 1] <int> ()
    }()

The :code:`$i` will change along the :code:`5` from 0 to 4. So above code is used to
describe such layout:
    
    int; int, int; int, int, int; int, int, int, int; int, int, int, int, int

In modified BNF, this can be descirbed as::

    block-number ::= expression (";" "~"variable)
    expression   ::= (number | variable) | function (("+" | "-" | "*" | "/" ) expression)?
    number       ::= [0-9]+
    variable     ::= "$" [a-zA-Z]+ [0-9]* | "@" [a-zA-Z]+ [0-9]*
    function     ::= "$" [a-zA-Z]+ [0-9]* "(" arguments ")"

:code:`number`
    A number must great equal to zero.

:code:`variable`
    A variable begined with "$" is scale variable, it can refer to a number, a function
    or a file handle. A variable begined with "@" is a array, which content 0 or more numbers.
    see variable for more information.


unit-block
-----------------------

The :code:`unit-block` is used to represent what the uint is. It indicate the size/type of
one block, the value of the block, and which variable the value of the block will assinged
to.

The :code:`uint-block` multiplied by :code:`number-block` will be a :code:`segment`.

In modified BNF::

    block-uint ::= uint (";" "=" (expression | "{" choice "}" | "[" array "]") | "(" range ")")?  (";" "=:" (expression)? (";" ":"variable)? (";" ":+"variable)
    uint       ::= "bit" | "byte" | "char" | "uint8" | "int8" | "uint16" | "int16" |
                   "int" | "uint32" | "int32" | "uint64" | "int64" | "float" |"float32" |
                   "double" | "float64" | "ascii"
    choice     ::= expression ("," expression) +
    array      ::= expression ("," expression) +
    range      ::= expression "," expression



For plaintext, :code:`uint` can be a :code:`ascii`.

If :code:`uint-block` have a :code:`"=" expression part`, this is mean the value of :code:`expression`
is the value of this block.

For example:

    [%let $n = 3]<>()
    [8]<int; =$n * 2>(dsp="the int block has a value 6")

The "=" can follwed by a :code:`choice`.

For example:

    [5] <float; ={1.0, 2.0, -9}> (dsp="float value can be anyone of it's choices")

The :code:`array` is values which would assigned to blocks, if the lenth of this array is
greater than block number, only front value be used, if it shorter than block-number, the arrary
will be repeated.

The :code:`range` is used to limit value's range of the block.

And the blocks can assigned a array varible too, same like a array.

For example::

    [3] <int; =[1, 2, 3]> (dsp="this segment have 3 blocks, them have value 1, 2, 3")
    [3] <int; =([5, 10))> (dsp="the value block set between 5, 10, and 5 is included")
    [%let @ar = [1, 2, 3]] <> ()
    [5] <int; =@ar> (dsp="the segment will be 1, 2, 3, 1, 2")

Some time the vaule assign to a block only can be decided after the assignment. And
for this case, using "=:" as a delay assignment.

For example::

    [%let $n = 0] <> (dsp="$n is initiated with 0")
    [1] <uint64; =:$n> (dsp="$n would decided after this assignment")
    [4] <int; :+$n> (dsp="this sagment have 4 block, the value as added to $n")
    
The value can be assigned to a value, or stored by a array.

For example::

    [1] <int; :$i> (dsp="the value of block is assigned to $i")
    [$i] <char> (dsp="the number of char is decided by int behind this segment")
    [$i] <float; :@collector; :+$float_sum> (dsp="all floats of this segment was stored by @collector
        the float value is added up to $float_sum")

In above example, the value of floats is collected by :code:`@collector` and the sum of all floats is
add up to :code:`$float_sum`, here we use ":+" to reprent this operation.


description
-------------------------

:code:`description` is a group of descreption :code:`segment`.

In modified BNF::

    description     ::= label-name "=" '"' value '"' (";" label-name "=" '"' value '"') *
    label-name      ::= [a-ZA-Z] +
    value           ::= [a-zA-z\s] +


description is consist of :code:`label-name` and :code:`value`. The :code:`lable-name` is predefined
by FLML or user can define it as need.

Here is a same example::

    [%fileinfo]<>(dsp="this is a file", type="text")




Variables and expression
==========================


Descreption labels
===========================


Key words
============

All key words of FLML begain with "%". That is::

    key-words ::= "%let", "extern", "%file",
                  "%deflabel", "%include", "%extend", "%block",
                  "%if", "%elif", "%else", "%for", "%while",
                  "%assert", "%warning", "%error", "%message"
                  "%break", "%continue"
                  "%deffunc"

:code:`%let`
    Used to declare and assign value to a variable.

    For example::

        [%let $var = 5]<>()
        [%let @arr = [1, 2, 3, 4]<>()

:code:`%extern`
    Declare a variable which is defined out of present file.

:code:`%file`
    Declare a variable is file type.

    For example::

        [%file $a_file]<>(dsp="a plaintext file")

:code:`%deflabel`
    To define a new label.

    For example::

        [%deflabel newlabel]<>(dsp="This is a new label")

:code:`%if %elif %else`
    To structure a branch.

    For example::

        [%let $var = 5]<>()
        [%if $var > 5]{
            [3]<int>()
        }()
        [%elif $var == 5 ]{
            [100]<char>()
        }()
        [%else]{
            [5]<float>()
        }()

:code:`%for %while`
    To structure a loop.

    For example::

        [%let $i = 0]<>()
        [%for ($i = 0; $i < 10; $i = $i - 1)] {
            [1]<int; +$sum>()
        }
        [%i = 15]<>()
        [%while $i > 10] {
            [1]<int; @collector>()
            [$i = $i - 1]<>()
        }()

:code:`%assert`
    To assert something.

    Example::

        [%assert $i > 3]<>()


:code:`%message`
    To message some information as remainder.

    Example::

        [%message "This is not right"]<>()


:code:`%deffunc`
    Define a function.

    Example::

        [%deffunc $myfunc ($va, $vb) $res]{
            [$res = $va + $vb]<>()
        }()






Branch
================


Loop
============


Function
==============


Comment
===============


Built in functions
======================


Standard lables
==================


Examples
================



    key wrods of MLBF all begined with `%`.

    :code:`%let`

        declare a variable, and assign value.

        example:
        
        :code:`[%let $var = 3]<>()`

    :code:`%extern`

        declare a variable, and the value of this value is offered by user.

        example:

        :code:`[%extern $var]<>(mesg="this value is assigned by user.")`

    :code:`%file`

        assign a file reference to a variable.
    
        example:

        :code:`[%file $file_ref]<>(file="a descreption of file which refered to")`


    :code:`%if %elif %else`

        key words used to flow control.

        example:

        .. code::

            [%let $var = 3]<>()
            [%if $var >= 0]{
                [$var]<int>()
            }()
            [%elif $var < 0]{
                [5]<int>()
            }()
            [%else]{
                []<>(mesg="this is not possible")
            }()

    :code:`%for`

        for loops.

        example:

        .. code::

            [%let $var = 0]<>()
            [%for $i = 1; $i < 10; $i++]<$var += $i>()

            [%for $i = 0; $i < 5; $i++]{
                []<$var *= $i>()
            }()

    :code:`%while`

        while loops.

        example:

        .. code::

            [%let $i = 3]<>()
            [%while $i > 0]<$i -= 1>()

    :code:`%error`

        indicate a error.

        example:

        :code:`[%error]<>(mesg="this is a error message")`

    :code:`%warning`

    :code:`%assert`

        assertion.

        example:

        :code:`[%assert $var == 3]<>()`


    :code:`%break and %continue`

        pass or break within loops.

        example:

        .. code::
            
            [%let $var = 1]<>()
            [%while 1]{
                [%if %var > 10]{[%break]<>()}()
                [%if $var == 2]{
                    []<$var += 2>()
                    [%continue]<>()
                }()
                []<$var += 1>()
            }()

    :code:`%func`
        
        used to declare a function. see following.
    
    :code:`%note`

    :code:`%mesg`

    :code:`%extend`

    :code:`%include`

    :code:`%block`

3. expression
-------------------


4. function
-------------------
.. code::

    [%func $func_name(%args1, %args2)$return_value]{
        []<$return_value = $args1 + args2>()
    }()



5. build in function
-----------------------

    $filelen

    $filesize

    $append()

    $ceil

    $floor

    $sum


6. comment
--------------------

    [#]<>()

    [#\*]<>()
    [\*#]<>()


7. standard lables
--------------------------

    info

    file

    id

    dsp

    order


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
