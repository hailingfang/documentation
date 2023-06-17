============================================
Reference of File Layout Markup Language 
============================================

version: 1.0.2; by Benjamin Fang

creat: 20230401; update: 20230617

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
    [1] <int; $x> (dsp="one int, the value stored by this int is assigned to variable $x")
    [$x] <float> (dsp="the amout of float is $x")

This example described the data type and the number of each type. :code:`dsp` is a
label to give information about :code:`[]<>` part.

Syntax
==================

An FLML description is composed of FLML sentences. Each sentence is formatted as either
:code:`[square-bracket-part] <angled-bracket-part> (round-parenthese-part)` or
:code:`[square-bracket-part] {curly-bracket-part} (round-parenthese-part)`.

The primarily role of the
:code:`square-bracket-part` part is to describe the number of :code:`block`. The :code:`angled-bracket-part` is used to
recorde the :code:`block` type(or say data type). And the last part, within :code:`round-parenthese-part`
is made up of several labels, in form :code:`label=value`. These labels and their values are
used to descirbe the :code:`[] ()` part. :code:`curly-bracket-part` is made up of FLML statments.

Using a modified BNF grammar notation. Which can be defined as::

    flml-description   ::= flml-statment +
    flml-statment      ::= "[" square-bracket-part "]" ( "<" angled-bracket-part ">" | "{" flml-statment "}" ) "(" round-parenthese-part ")"


Terminology
---------------

* sentence
    A FLML sentence looks like :code:`[statment]<statment>(statment)` or :code:`[statment]{sentences}(statament)`.
    A sentence is have tree **sentence parts**, the first one is called "square bracket part",
    which include the "[]" marker and statments it containing.
    The second is called "angled bracket part" or "curly bracket part". The last is called "round parenthese part".

* statment
    A statament in FLML is a expression end by ";". If the statament is last one of a sentence part. the ";" can be omiited.

* block
    A block is the uint which construct the further data structure. For instance, :code:`[8] <int> ()` (example A),
    where the "int" is the block, which is inclose by a "<>" parenthese. The main function of "angled bracket part" and
    "curly bracket part" is to contain block.

* sample block and complex block
    The block can de divided into two tipies: sample block and complex block. A sample block is
    a basic data type which have beed define in this language, which can not consist of other
    blocks. For example, the "int", "float", "char" all are sample blocks. The sample block was enclosed
    by "<>". The complex block, on the other hand, is made up of sample blocks. For example, :code:`[3]{[1]<int>() [1]<float>()}()` (example B).
    The complex block in the example is consist of one int and one float. The complex block is enclosed by
    "{}"

* block type
    There many kinds of sample block type, each type reprent the its data type as well as data size. For example,
    A "uint64" sample block meant that the data is a integer and it consums 64 bits.

* block size
    For a given block, no matter it is a sample block or complex block, the size of it is decided.
    that is the size of block, or in term, block size. For the example I given above, the block size
    of "{[1]<int> [1]<float>}" is 8 bytes (here we suppose the size of int is 4 bytes).


* block multiplier
    There is a number or variable in "[]" to indicate the amount of block. For example A which given above,
    "[8]" mean there are 8 "<int>". The number "8" here is a block multiplier, which use to represent the
    repeated time of the block.

* segment
    The block multiplied by multiplier of same sentence makes a segment. For example A, :code:`[8]<int>()` make a segment, which have 8 int,
    the the size is 32 bytes. The block makes a sagments also called the **element** of segment. The multiplier also termed
    the length of segment or **segment length**.



Square bracket part
-----------------------

:code:`square-bracket-part` is the first part of FLML sentence, which mainlly used to describe the number of block.
This part is made of statment enclosed by "[]". The part have four types of stetments.

1. A statament indicate the number of block

This statament is a expression, the value of the expression is number of block, In Terminology, this value
is the multiplier of block or length of the segment.

For example::

    [3] <byte> ()
    [%let $num = 5] <> ()
    [$num * 2] <float> ()

For the first sentence in the example above, the block is "byte", and multiplier is 3.
which make a segment of 3 bytes. The second sentence defined a variable, whose value is 5.
And in the third sentence, the statament in square bracket part is a expression having a value 10,
The the multiplier is 10, the segment is 10 floats sagment. 


2. A variable iteration statament.

Along with multiplier, there can be a **iteration statament**. which made of "~" followed by variable.
(a variable is words start with "$" or "@").

For example::

    [3; ~$i] {
        [$i] <float> ()
        [2] <int> ()

    } ()

In the example, The "~$i" is a iteration statament, The $i will iterated from 0 to 3 in
its element. The block of sentence is complex block, the complex is descirbed by two sentence,
The segment have 3 block, the first block is made of 0 float 2 integers, and second is made of 1 float
2 integers. The third is made of 2 floats 2 integers.

3. A order collecting statament. 

Some time the order of a sequece is importand and the order may be aligned by following segment.
The statament is used to collect the order, or refer the order of a sagment.

For example::

    [10; ^@myorder] <string> ()
    [10] <int> (alignwith=@myorder)
    [10; ~$i] {
        [1] <float> (order=@myorder[$i])
    } 

4. statament of FLML operation

This kind of statament is operation of FLML, such as declear a variable, branch and loop and so on.

For example::

    [%let $var = 3]
    [%if $var == 2] {
        [1] <int>
    }

.. In modified BNF, The  can be descirbed as::

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

All key words of FLML begain with "%".


* %let

* %if %elif %else

* %for

* %while

* %deffunc %return

* %deflabel

* %assert

* %mesg

* %error

* %infor

* %file

* %parse

* %include

* %extern

* %define


Block type
---------------------

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

* Plaintext.

.. code::

    <char> <string> <ascii>

the :code:`<ascii>` was used to reprent asscii code, the block/unit consums 1 byte.


Built in functions
-------------------------

* $getorder

* $sum

* $abs

* $floor

* $ceil

* $filelinenum

* $filesize

* $abs



Standard lables
--------------------

* dsp

* ele-dsp

* value-dsp

* value

* NA

* name

* filetype

* endianness

* datatype

* order

* alignwith

* sep

* end

* encode

* re

Specicial variable
------------------------

* $?

* $*

* $+

* $NA

* $NONE

* $UNKNOW

* $WHITESPACE

* $EOF

* $NEWLINE

* $TAB

* $EXTARGS

* $INFINITY

* $TRUE

* $FAUSE
