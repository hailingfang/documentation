======================================================
Reference of File Layout Markup Language 
======================================================

version: 1.1.0; by Benjamin Fang

create: 20230401; update: 20230627




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

    3 integers; 1 char, whose value is 255; 1 integer which have a value "X"; "X" floats.

You can describe the layout using FLML like following::

    [3] <int> (dsp="3 integers")
    [1] <char; =255> (dsp="one char, whose value is 255")
    [1] <int; $x> (dsp="one int, the value stored by this int is assigned to variable $x")
    [$x] <float> (dsp="the amount of float is $x")


An FLML description is composed of FLML sentences. Each sentence consist of three parts:
:code:`[square-bracket-part] <angled-bracket-part> (round-parenthese-part)` or
:code:`[square-bracket-part] {curly-bracket-part} (round-parenthese-part)`.

The primarily role of the :code:`square-bracket-part` part is to describe
the number of :code:`block`. The :code:`angled-bracket-part` is used to
recorde the :code:`block` type(or say data type). And the last part, within :code:`round-parenthese-part`
is made up of several labels, in form :code:`label=value`. These labels and their values are
used to descirbe the :code:`[] ()` part. :code:`curly-bracket-part` is made up of FLML sentences.

In above example, the first sentence is :code:`[3] <int> (dsp="3 integers")`. The "3" in "[]" is reveal the
number of block which is a "int" written in "<>". "dsp" in "()" is a label, which is used to offer
information about square-bracket-part and angled-bracket-part/curly-bracket-part.

Using a modified BNF grammar notation. Which can be defined as::

    flml-description   ::= flml-sentences +
    flml-sentences     ::= "[" square-bracket-part "]" ( "<" angled-bracket-part ">" | "{" flml-sentences "}" ) "(" round-parenthese-part ")"




Data types
========================
There are two data types in FLML, one is scaler and the other is array. scaler can refer to number, file, and iterater, and
a order element. On the other hand, array is a collection of scaler.

A scaler variable, which is used to reprent a scaler, is start with "$", and a array variable is start with
"@".

Here are some examples.

.. code::

    $sca = 3;
    @arr = [1, 2, 3, 4, 5];
    $sca = @arr[0]; // $sca equal 1
    @arr[:2] = [7, 8];

Array can be indexed and sliced, "@arr[0]" refers to the first element of the array, while "@arr[:3]" refers to
a range form the first to the third. 

In BNF::

    variable ::= "$" [a-zA-Z*+?] + [0-9]* | "@" [a-zA-Z]+ [0-9]*




Operator, expression and statement
==========================================

The operator of FLML include :code:`+ - * / : ~ ^ =` The "+ - * /" is same as normally
itself in algebra. For example::

    $foo = 1 + 3; // $foo equal 4
    $foo = 4 - 3; // $foo equal 1
    $foo = 4 * 3; // $foo equal 12
    $foo = 5 / 2; // $foo equal 2.5

There are five operator in FLML, they are "+ : ~ ^ =". They have sepecial meaning in certain context.

A expression of FLML is consist of variables and operators. and a expression end with a ";" make
a statament.

In BNF::

    statament  ::= expression ";"
    expression ::= (operator)? (variable | number) (operator expression)?
    variable   ::= "$" [a-zA-Z*+?] + [0-9]* | "@" [a-zA-Z]+ [0-9]*
    number     ::= [1-9]+ "." [1-9]
    operator   ::= [+-*/:~^]




FLML sentences
========================

Terminology
---------------

* statment
    A statament in FLML is a expression end by ";". If the statament is last one of a sentence part. the ";" can be omiited.

* sentence
    A FLML sentence looks like :code:`[statment]<statment>(statment)` or :code:`[statment]{sentences}(statament)`.
    A sentence is have tree **sentence parts**, the first one is called "square bracket part",
    which include the "[]" marker and statments it containing.
    The second is called "angled bracket part" or "curly bracket part". The last is called "round parenthese part".


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

* segment, segment length, elements of segment
    The block multiplied by multiplier of same sentence makes a segment. For example A, :code:`[8]<int>()` make a segment, which have 8 int,
    the the size is 32 bytes. The block makes a sagments also called the **elements** of segment. The multiplier also termed
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


2. Iteration operator and iteration statament.

Along with multiplier, there can be a **iteration statament**. which made of "~" followed by variable.

For example::

    [3; ~$i] {
        [$i] <float> ()
        [2] <int> ()

    } ()

In the example, The "~$i" is a iteration statament, The $i will iterated from 0 to 3 in
its element. The block of sentence is complex block, the complex is descirbed by two sentence,
The segment have 3 block, the first block is made of 0 float 2 integers, and second is made of 1 float
2 integers. The third is made of 2 floats 2 integers.

3. Order collecting operation and order collecting statament. 

Some time the order of a sequece is importand and the order may be aligned by following segments.


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

.. note::
    
    multi FLML statement can be writren within one square bracket.

In modified BNF, it can be descirbed as::

        square-bracket-part ::= (expression (";" "~"variable)? (";") "^"variable ) | other statament 


Angled bracket part
-----------------------

:code:`angled-bracket-part` is mainlly used to offered block information. It also have
some additional stataments.


1. a string represent block tpye.

For example::
    [1] <float> // block type is float
    [1] <uint32> // block type is int, whose size is 4 bytes


2. A statament only have a variable.

For example::

    [1] <int; $int_value>  // value of this block is stored in $int_value
    [3] <float; @float_values> //this segment have 3 float, the values of those floats were stored in @float_values

If the length of segment is one, the data type of variable should be scaler, otherwise, it should be a array.

There are a typea operator can be applied to this variable: accumulating operator "+".

"+" will keep the value already stored by the variable, and add the new value up to the original.

For example::

    [10] {
        [1] <int; +$sum>
    
    }
    
This will add 10 value to $sum.


3. Assign a value to the block

We can assign one or more value to a segment.

For example::

    [1] <int; =2>
    [4] <int; =[1,2,3,4]>
    [%let $a = 5]
    [%let @b = [1, 2, 3]]
    [1] <int; =$a>
    [3] <int; =@b>


4. A choices of block.

For example::

    [8] <char; =0> (dsp="this segment has 8 blocks, and the value of block is 0")
    [4] <int; ={0, 1}> (dsp="this segment have 4 int, the value of block should be either 0 or 1")


In modified BNF::

    angle-bracket-part ::= block-type (";" variable)? | (";" "+"variable) (";" ("=" | "=:") variable)? (";" "=" choices | range | value_list)?
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




Declearation of new variable
==============================
"%let" can be used to declear a new variable. For example::

    [%let $a = 3]

The new declear variable can initiated like what we do in example.

A variable can auto declear when it show up first time. For example::
    [1] <int; $bar>

The variable "$bar" is decleared and the value of the block is assigned to it.




Branch
========================

The Branch in FLML used key words :code:`%if %ifel %else`.

The usage is::

    [%if expression] {
        sentences
    } ()
    
    [%elif expression] {
        sentences
    } ()

    [%else] {
        sentences
    } ()




Loop
========================


1. The "for" loop

The usage of for statment is::

    [%for expression_a; expression_b; expression_c] {
        sentences
    } ()


The for loop is just like C's.

For example::

    [%let $sum = 0] <> ()
    [%for $i = 0; $i < 10; $i ++] {
        [$sum += $i] <> ()
    } ()


2. The "while" loop

The usage of while loop::

    [%while expression] {
        statments
    } ()




Function
============================

The way to define a function::

    [%deffunc $funname (arguments) returns] {
        sentences
    } ()

Here is an example::

    [%deffunc $myadd ($a, $b) $c] {

        [$c = $a + $b] <> ()
        [%return $c] <> () 

    } ()

The [%return] can be omitted.




Comment
===========================

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




Omission
========================

A FLML must have a square bracket part. The angle bracket part and round
parenthesis part can be omiited if they have no contents.  

Examples::

    [%let $sum = 0]
    [%for $i = 0; $i < 10; $i++] {
        [$sum += $i]
    }




" " and ' ' in FLML
==============================

"" and '' can be used to parenthesis a string. The difference between them is that
the variable within "" would be extended, the other is not. The specifier like "\n", "\t"
would refer to a new line and tab respectively too.

For example::

    [%let $var = 3; %let @arr = [1, 2, 3]]
    [%mesg "\$var is $var"] //the mesg is: $var is 3
    [%mesg 'this is @aarr'] // the message is: this is @arr




Appendix
===========


Key words
-------------

All key words of FLML begain with "%".


* %let

    Declear a variable and initiate it.

    .. code::

        [%let $var = 12]
        [%let @arr = [1, 2, 3]]

* %if %elif %else

    Those three key words is used in loop.

    ..code ::

        [1] <int; $var>
        [%if $var > 10] {
            [10] <int>
        }
        [%elif $var == 10] {
            [5] <int>
        }

        [%else] {
            [1] <int>
        }


* %for

    To construct for loop sentence.

    .. code::

        [%let $var = 10]
        [%for ($i = 0;$i < 10; $i += 1)] {
            [$var]
        }

    If no other stataments, the parenthesis of "%for" can be omiited.


* %while

    To make whild loop sentence.

    .. code::

        [$let $var = 10; %let $summ = 0]
        [%while $var > 0] {
            [1] <int; +$summ>
            [$var -= 1]
        }


* %break %continue

    Those key words used in loop.

* %assert

    Assert a statament.

    .. code::

        [%assert $var == 0]

* %error

    Give error information.

    .. code::

        [%error "this is a error"]

* %mesg

    Give a message.

    [%mesg "this a message"]


* %deffunc %return

    When use "%deffunc" to define a function, all "[]" can be omitted.
    The arguments of function put into a parenthesis and saperated by commer.
    Then the variable will be return followed the arguments. The "%return" statament
    can be omiited.
    function should be defined before refered to. You can declear the function first and
    then define it later like C language.

    .. code::

        [%deffunc %myfunc ($var_a, $var_b) $data_out]

        [%let $a = 13; %let $b = 14; %let $c = $myfunc($a, $b)]
        [$mesg "the value of \$c is $c"]
        [$c]<float>

        [%deffunc %myfunc ($var_a, $var_b) $data_out] {
        
            %let $c = $var_a + $var_b;
            $data_out = $c;
            %return %data_out; // can be omitted
        }


* %info

    Give information, Generally, use it to offer information about whole file.

    .. code::

        [%info](dsp="a binary file"; filetype="binary"; endianness="little")


* %file

    declear a variable which refer to a file.

    .. code::

        [%file $file_var "file description" "file_name"]
    
    The "file name" can be omiited.

* %parse

    To parse an array. 

    .. code::

        [100]<byte; @data_a>
        [%let @data_b = %transform(@data_b)]

        [%parse @data_b] {

            sentences
        
        }


    The original data in the file maybe need some transform and the transformed data
    have acctual meaning. When is the time "%parse" works.


* %deflabel

    Used to define a new label user itself.

    .. code::

        [%deflabel newlabel "this is a new label used to express new attribute"]

.. * %define

.. * %include

.. * %extern


Block type
-------------------------

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

* $abs

    .. code::

            %let $a = -2;
            %let $b = $abs($a); // $b equal 2

* $floor

    .. code::

        %let $a = $floor(10 / 3); // $a equal 3

* $ceil

    .. code::

        %let $a = $ceil(10 / 3); // $a equal 4

* $sum

    .. code::

        %let @arr = [1, 2, 3];
        %let $ss = $sum(@arr); // $ss equal 6

* $append

    .. code::

        %let @arr = [1, 2, 3];
        %let $a = 4;
        $append(@arr, $a); // @arr is [1, 2, 3, 4]

* $pop

    .. code::

        %let @arr = [1, 2, 3];
        %let $a = $pop(@arr); // @arr is [1, 2], $a equal 3

* $length

    .. code::

        %let @arr = [1, 2, 3];
        %let $a = $length(@arr); // $a is 3


* $getorder

    Get the order of a file or array.

    .. code::

        %file $test_file "a test file"
        %let @order = $getorder($test_file); // @order represent the order of file.


* $filelinenum

    Return the line number of a plaintext file.

* $filesize

    Return size of file.


Standard lables
--------------------------

* dsp

    Description of segment. This label is used for general popurse and have no limitation.
    The value is a string.

    .. code::

        dsp="string"

* ele-dsp

    Description the element of segment. The value is string.

    .. code::

        dsp="string"

* value-dsp  value

    Description the mean of each value.

    .. code::

        [1] <char; ={0, 1, 2}> (value-dsp="descripiton of value"; value={0: "dsp one", 1: "dsp two", 2: "des three"})


* NA

    Value to indicate NA.

* name id

    name of segment.

* filetype

    File type, vlaue is "binary" or "plaintext".

* endianness

    endianness of file, value is "little" or "big".

* order alignwith

    The order which the block refer to.

    .. code::

        [%file $myfile "my file"]
        [%let $filelen = $filelinenum($myfile)]
        [@let @order = $getorder($myfile)]
        [1] <int> (order=@order[0])
        [$filelen] <float> (alignwith=@order)

* datatype

    Used in plaintext descripiton, reprent the data type of block.

* sep

    Used in plaintext descripiton, the seperator between elements of segment.

* end

    Used in plaintext descripiton, reprent the end of segment.

* encode

    Used in plaintext descripiton, reprent the encoding type of plaintext.

* re

    Used in plaintext descripiton, indicate whether the regular express is used or not.


Specicial variable
------------------------

* $*

    This variable refer to a range [0, infinity).

* $+

    This variable refer to a range [1, infinity).

* $?

    This variable refer to a value, which is 0 or 1.

* $NA $NONE $UNKNOW

    The variable means that the value is not known.

* $WHITESPACE

    Refer to "\s" or "\t".

* $EOF

    Refer to End Of File.

* $NEWLINE

    Refer to "\n".

* $TAB

    Refer to "\t".

* @EXTARGS

    Refer to a array, which store arguments of command line. This is defined for future usage.

* $INF $INF_POS $INF_NEG

    Refer to a infinity value.

* $TRUE

    Refer to true.

* $FAUSE

    Refer to false.