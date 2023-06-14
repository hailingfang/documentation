============================================
Reference of File Layout Markup Language 
============================================

version: 1.0.1; by Benjamin Fang

creat: 20230401; update: 20230614

Introdution
======================

In my work in software development, I often need to parse files,
which can be either binary or plaintext. To understand the structure and
content of these files, I typically refer to documentation in the form
of descriptive text or tables that outline the meaning of each field and
its associated data type. My goal is to create an easy-to-use and accurate
markup language that can be used to describe the layout of both binary and
plaintext files. Once I have designed this language, I plan to use it to
document commonly used file formats in the biological field and other areas. 

This method is simple. For example, if you want to describe a binary file organized as follows::

    3 integers; 1 char, which value is 255; 1 integer which have a value "X"; "X" floats.

You can describe the layout using FLML like following::

    [3] <int> (dsp="3 integers")
    [1] <char; =255> (dsp="one char, whose value is 255")
    [1] <int; :$x> (dsp="one int, the value stored by this int is assigned to variable $x")
    [$x] <float> (dsp="the amout of float is $x")

This example described the data type and the number of each type. :code:`dsp` is a
label to give information about :code:`[]<>` part.

Syntax
==================

An FLML description is composed of FLML statments. Each statment is formatted as either
:code:`[square-bracket-part] <angled-bracket-part> (round-parenthese-part)` or
:code:`[square-bracket-part] {curly-bracket-part} (round-parenthese-part)`.

The primarily role of the
:code:`square-bracket-part` part is to describe the number of unit. The :code:`angled-bracket-part` is used to
recorde the unit type(or say data type). And the last part, within :code:`round-parenthese-part`
is make up of several labels, in form :code:`label="value"`. These labels and their values are
used to descirbe the :code:`[] ()` part. :code:`curly-bracket-part` is made up of FLML statments.

Using a modified BNF grammar notation. Which can be defined as::

    flml-description   ::= flml-statment +
    flml-statment      ::= "[" square-bracket-part "]" ( "<" angled-bracket-part ">" | "{" flml-statment "}" ) "(" round-parenthese-part ")"


Terminology
---------------

There I define some terms in order to clarify my expression.

The uint represented by :code:`angled-bracket-part` is called :code:`block`;
The number recorded within :code:`square-bracket-part` is call :code:`segment-length`;
While the block repeat :code:`segment-length` times, or say: :code:`segment-length` multiply block, those multiplied blocks composed
a :code:`segment`.


square-bracket-part
-----------------------

:code:`square-bracket-part` is mainlly used to describe the number of :code:`angled-bracket-part`.
It can also be a container of statment, like "%let", "%if" and so on.


1. :code:`square-bracket-part` can be a expression, the value of expression is number of :code:`block`.

For example::

    [3]<byte>(dsp="this FLML give information that this is a 3 bytes segment")
    [%let $num = 5]<>()
    [$num * 2]<float>(dsp="this segument contain 10 blocks, each block is a float")

2. :code:`seqare-bracket-part` can be a container of some statments.

For example::

    [%let $i = 3] <> (dsp="assign value to $i")
    [%if $i == 3] {
        [16]<uint32>()
    } (dsp="if the value of $i is equal to 3, the segments within {} will exist in the file")
    [%else] {
        [%error "this is a error"] <> ()
    } (dsp="if $i is not equal to 3, this would be a error")


3. :code:`square-bracket-part` could have a additional specicial variable called  iteration variable.

For example::

    [5; ~$it] {
        [$it + 1] <int> (name="segmentB")
    } (dsp="$it will change from 0 to 4"; name="segmentA")


The value of $it is change form 0 to 4, so the sagment-length within {} should be
1, 2, 3, 4, 5 respectively. So, :code:`sagmentA` has 5 :code:`block`, and each
block is a segment, named :code:`segmentB`, the block of segmentB is int, and the
:code:`segment-lenth` is $it, and $it is a iteration variable, it changed over each
segmentB. 


In modified BNF, The  can be descirbed as::

    square-bracket-part ::= (expression (";" "~"variable)?) | ( keyword expression) 
    expression          ::= (number | variable) | function (("+" | "-" | "*" | "/" ) expression)?
    number              ::= [0-9]+
    variable            ::= "$" [a-zA-Z]+ [0-9]* | "@" [a-zA-Z]+ [0-9]*
    function            ::= "$" [a-zA-Z]+ [0-9]* "(" arguments ")"
    keyword             ::= "%" [a-zA-Z]+ [0-9]*



angled-bracket-part
-----------------------

:code:`angled-bracket-part` is mainlly used to offered block information. It also have
some additional variables that have other functions.


1. :code:`angle-bracket-part` represent block tpye.

For example::
    [1] <float> (dsp="the block type is float, one float comsume 4 bytes")
    [1] <uint32> (dsp="a 32 bits block")

2. The value of block can be assigned to a variable.

For example::

    [1] <int; :$len> (dsp="the value of the block is assigned to $len")
    [$len] <float> ()

3. A value can assigned to the block.

For example::

    [8] <char; =0> (dsp="this segment has 8 blocks, and the value of block is 0")
    [4] <int; ={0, 1}> (dsp="this segment have 4 int, the value of block should be either 0 or 1")


In modified BNF::

    angle-bracket-part ::= block-type (";" (":" | ":+") (variable))? (";" ("=" | "=:") (variable | choices | range | value_list))?
    choices            ::= "{" elements "}"
    range              ::= "(" ("(" | "[") range-start ","  range-end ("]" | ")" ) ")"
    value_list         ::= "[" elements "]"
    elements           ::= variable ("," variable)*



curly-bracket-part
----------------------

When the :code:`block` is not a sample block type, such as int, float and so on, instead
it is some other :code:`segment`. the curly bracket is used to contain those segment. The
other applicaiton of curly-bracket-part is used for complex statments like :code:`[%if 1]{}()`.

1. used when block is a segment.

For example::

    [6] {
        [2] <bit> ()
        [3] <int> ()
    } (dsp="the block is sagment, the sagment is 2 bits and 3 int")


2. used when a complex statment introduced.

For example::

    [%for $i = 0; $i < 10; $i++] {
        [$i + 1] <int> ()
    } (dsp="$i changed from 0 to 9")

By the way, this example can be replace by other way::

    [10; ~$i] {
        [$i + 1] <int> ()
    } ()



round-parenthesis-part
-------------------------

:code:`round-parenthesis-part` contain labels that used to descirbe the :code:`segment` or :code:`block`.

For example::

    [1] <char; =2> (dsp="this is a example"; value="1 for fou, 2 for bar"; name="example-segment")


The lable is pre-defined by FLML, the user can define label themself by :code:`[%deflabel mylabe "this is my label"]<>()` too.


In modified BNF::

    description     ::= label-name "=" '"' value '"' (";" label-name "=" '"' value '"') *
    label-name      ::= [a-ZA-Z] +
    value           ::= [a-zA-z\s] +


Variables and expression
============================

FLML have two kinds of variables: :code:`scaler` and :code:`array`. The scaler refer to a
number, a function or a file. while the array is refer a bunch of scalers. Scaler varialbe start with a "$",
and array start with a "@".

* Here is some examples of scaler::

    [%let $a = 3] <> ()
    [%let $b = 2] <> ()
    [$a] <int> (name="seg1")
    [$a + 2 * $b] <float> <name="seg2">

    [1]<int; :$c> (name="seg3")
    [10] {
        [1] <int; :+$d> ()
    } (name="seg4")
    
    [1] <int; =$a> (name="seg5")
    [1] <int; =:$a> ("name="seg6")
    [$a = $a + 5] <> ()

    [10; ~$e] {
        [$e] <char> ()
    } (name="seg7")

    [$myfun($a, $b)] <int> (name="seg8")
    [%file $file_handle "file description"] <> (name="seg9")

Example "seg1" and "seg2" is the basic usage of scaler. It refer to a number.
In example "seg3", scaler follows a marker ":", this mean the value of block is assigned
to this variable.

Example "sag4", the variable follows ":+", this a accumulating assing, and this mean
the values of will added to the variable.
The "seg5" assign the value of $a to the block.
The "seg6" example, "$a" follows "=:", this is a later assign sign, the value would be used late "$a", it is 8 here, instead
the old(3).

In example "seg7", "$e" follows "~", this is a iteration sign and make "$e" a iteration variable.
In "seg8", the "$myfun" refer to a function. In "seg9", the variable refer to a file.


* Here is some examples of array::

    [%let @ar1 = [1, 2, 3]] <> (name="seg10")
    [@ar1 * 3] <float> (name="seg11")

    [10] <int; :@ar2> (name="seg12")
    [3] <int; =@ar1> (name="seg13")

    [@ar1; ~$i] {
        [$i] <float> ()
    } (name="seg14")


In example "seg10", a array named "ar1" was assigned with [1,2,3].
The next example name "seg11", this segment contain tree blocks, the first block is
is segment have 3 floats, the second is a segment contain 6 floats, the third segment
have 9 float. This example have same meaning of "seg14".

In example "seg12", the value of int was appended to "@ar2". In the "seg13", values
within "@ar1" was assigned to blocks.


In above examples, The example was shown too. The expression of FLML is same as C programming
language. The operation include :code:`+ - * /`. The assignment to a array using :code:`[]`.


In modified BNF::

    variable  ::= "$" [a-zA-Z]+ [0-9]* | "@" [a-zA-Z]+ [0-9]*




Branch
============

The Branch in FLML used key words :code:`%if %ifel %else`.

The usage is::

    [%if expression] {
        statments
    } ()
    
    [%elif expression] {
        statments
    } ()

    [%else] {
        statments
    } ()


Loop
============

1. the "for" loop

The usage of for statment is::

    [%for expression_a; expression_b; expression_c] {
        statments
    } ()


The for loop is just like C's.

For example::

    [%let $sum = 0] <> ()
    [%for $i = 0; $i < 10; $i ++] {
        [$sum += $i] <> ()
    } ()


2. the "while" loop

The usage of while loop::

    [%while expression] {
        statments
    } ()



Function
===========

The way to define a function::

    [%deffunc $funname (arguments) returns] {
        statments    
    } ()

Here is an example::

    [%deffunc $myadd ($a, $b) $c] {

        [$c = $a + $b] <> ()
        [%return $c] <> () 

    } ()

The [%return] can be omitted.


Comment
===========

1. comment like C language.

The comment in C style is acceptable.

Here is example::

    [1] <int> () //here is a comment
    
    //[3] <int> ()

    /*
        [3] {
            [5] {
                [5] <float> ()
            } ()
        } ()
    /*



2. segment comment.

"#" can be used for segment comment, to comment a segment.

For example::

    [# 10] {
        [1] <int> ()
        [1] <float> ()
    } ()




Omission of "<>" and "()"
===========================

If "<>" and "()" both don't have contents, then, them can be omitted.

If "()" don't have content, then it can be omitted.

Examples::

    [%let $sum = 0]
    [%for $i = 0; $i < 10; $i++] {
        [$sum += $i]
    }


Appendix
===========


Key words
-------------

All key words of FLML begain with "%". That is::

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



Block type
---------------------

* Plaintext.

    the :code:`<ascii>` was used to reprent asscii code, the block/unit consums 1 byte.

* integer

    The block type of integer include::

        <int8> <uint8> <char>
        <int16> <uint16> <short>
        <int32> <uint32> <int>
        <int64> <uint64> <long>

* float

.. code::

    <float> <float32> <float64> <double>

* bytes

.. code::

    <byte>

* bit

.. code::
    
    <bit>
    

Built in functions
-------------------------


Standard lables
--------------------