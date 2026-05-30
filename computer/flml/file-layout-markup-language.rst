======================================================
File Layout Markup Language Specification
======================================================

:Authors: Benjamin Fang
:Version: 2.0.0
:Create Date: 20230401
:Update Date: 20260529


Introdution
======================

File Layout Markup Language (FLML) is a markup language for describing the
layout/structure of binary or plaintext text files.


FLML Sentence
=====================
A sample FLML sentence have three parts: [...], <...> and (...).
Where the '...' reprent the stataments the parts hold.

There is a example of a FLML sentence::

    [5]<int>(name="sample sentence")

The '[...]' parts is necessary for a FLML sentence. The '<...>' and '(...)'
can be omiited.

A complex FLML sentence use '{...}' replace the '<...>' part.

For example::

    [2] {
        [2]<int>
        [1]<double>
        [8]<uint8>
    }(name="comple sentence")

The '{...}' can contain another '{...}'. If the value expression in
"[...]" equals 1, the '[...]' part before a '{...}' part can be omiited.

A FLML sentence start with '[...]', end before other '[...]'. Any blank
char between '[...]', '<...>', '{...}' and '(...)' is ignored.


The Data Types in FLML
=======================================

Number
-------------------

A number in FLML can be a integer, float or char. A char is a 8-bits
integer, and parenthesized by **''**.

Example::

    [123]
    [3.14159]
    ['A']

String
--------------------

String data type is support in FLML. The string should parenthesized by
**""**
Example::

    ["hello world"]

List
------------------

A list date type in FLML works same as the list date type in Pythons.

Example::

    [list_d = [1, 3, "aa", 4.6]]
    [list_d[1]]
    [list_d.append("hello")]

Dictionary
-------------------

A dictionary date type in FLML works same as the dictionary date type in Pythons.

Example::

    [dic = {"aa": 3, "bb": "hello", 3: 5}]
    [dic["aa"]]
    [dic["cc"] = 12]


Built in Functions
-------------------------

The built in functions of FLML include::
    
    sum(), len(), int(), str(), float().

The built in functions in Python may supported in FLML expression.

Example::

    [ld = [1,2,3];
     sum_num = sum(ld)]

The Variable and Expression in FLML
=======================================

The Variable
-----------------------

A variable in FLML consists of English characters, numbers or '_', and
can not start with a number.

For example::

    [aa]
    [bb13]
    [_cCd]

The Expression
--------------------------

A expression in FLML is composed by literal, variables and operators. 

Example::

    [x = 3 * 2 + 1]
    [y = x**2]

Arithmetic Operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The arithmetic operators'+', '-', '*', '/', '%' and '//' and '=' is supported.

Relational and Logical Operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

THe supported relational operators are '>', '>=', '<', '<=', '==', '!='.

The supported logical operators are '&&', '||', '!'.

Example::

    [a = 3;
     a > 1 && a <= 3]

Bitwise Operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The supported bitwise operators include::

    & bitwise AND
    | bitwise inclusive OR
    ^ bitwise exclusive OR
    << left shift
    >> right shift
    ~ one's complement

Example::

    [a = 31;
     a << 2]

The Statament
--------------------------

A statament is a expression end with ';'. The ';' of last expression in '[...]'
can be omiited.


The '[...]' Part
=======================

The '...' in '[...]' is one expression or many expressions(stataments).
If a FLML sentence have a '<...>' or '{...}' part. The '...' must can be calculated
and rusult with a integer value.

The integer value indicate the number of element. The element is repeated by '<...>'
or '{...}'. For instance, '[3]<float>', mean 3 elements, the element type is float.

The other instance::

    [2]{
        [2]<int>
        [4]<double>
    }

Means that there are 2 elements, every element is composed by 2 int and 4 double.

The '<...>' Part
=======================

The '...' in '<...>' is element type. It is used to indicate the data bit length.
The element types include::

    bit
    byte
    char, int8, uint8, int16, uint16, int, int32, uint32, int64, uint64
    float, double
    string

In '<...>', the value of element or elements can be assigned with a value or values.

Example::

    [1]<int; =19>
    [2]<char; =[5, 18]> 
    [4]<float; [2]=3.14>

The first line indicate the assignment of 19 to element. The second is the
assignment of 5, 18 to the elements. The third show how to assign 3.14 to the
third elemet of the data block.


In '<...>', a variable can be introduced to refer to element or elements representd by
sentences.

Example::

    [1]<int; :x>
    [2]<char; :y>
    [4]<float; [2]:z>
    [2]<uint16, =[23, 44]; :w>
The first use variable x to refer to the element in the block. The second is same as the
first, by y is list data type. The third using z to refer to third element of elements
representd by the sentence. In the fourth,w is [23, 44]. 


The (...) Part
=======================

The '...' in '(...)' are labels. The labels is (key, value) pares.
The labels record the additional information beyond '[...]' and '<...>'.
can recode.

Example::

    [3]<int; =[1, 22, 333]>(name="magice number";
                            id="mag_num";
                            greatthan=0;
                            lesseqthan=1000)

The labels defined in FLML::

    name        string  Name of block represented by the sentence
    id          string  Identity of the block, the string should start with
                        English characters or '_'. 
    dsp         string  descripiton
    greatthan   number  the element should great than a specific value
    lessthan    number  the element should less than a specific value
    greateqthan number  the element should great equal than a specific value
    lesseqthan  number  the element should less equal than a specific value
    choices     {items...}  items the element can be
    elementnum  the value calculated in '[...]' is number of element in '<...>' or '{...}' 
    offset      the value calculated in '[...]' is offset from begain of file
    bytelen     the value calculated in '[...]' is length of byte of block
    bitlen      the value calculated in '[...]' is length of bit of block


The Condition Sentence
============================

The stataments in '{}' will performed if corressponding Expression is true.

.. code::

    [if (Expression)] {
        FLML sentences
    } [elif (Expression)] {
        FLML sentences
    } [else] {
        FLML sentences
    }

    //or

    [
        if (Expression) {
            stataments
        } elif (Expression) {
            stataments
        } else {
            stataments
        }
    ]

Example::

    [1]<uint8; :x>(name="data type of next block", chiose={1, 2, 3})
    [if (x == 1)] {
        [8]<int>
    } [elif (x == 2)] {
        [8]<float>
    } [else] {
        [8]<double>
    }


The loop sentence
=============================

For Loop
-----------------------

.. code::

    [for (Expression)] {
        FLML sentences
    }

    //or
    [
        for (Expression) {
            stataments
        }
    ]

Example 1::

    [8]<int; :x>
    [for (i in x)]{
        [i]<int>
        [2 * i]<float>
    }

Example 2::

    [1]<int; :x>
    [for (i=0; i<x; i++)] {
        [i**2]<char>
        [5]<int>
    }

Whild Loop
-----------------------

.. code::

    [while (Expression)] {
        FLML sentences
    }

    //or

    [
        while (Expression) {
            stataments
        }
    ]

Example::

    [x = 3]
    [while (x)] {
        [x]<int>
        [4]<int; []=32>
        [1]<uint; :x>
    }


The jump sentence
============================

.. code::

    [goto offset] {
        FLML sentences
    }

    //or
    [
        goto offset;
    ]

The offset if offset from file's begaining in byte.

Example::

    [x = 1024]
    [goto x]{
        [2]<int>
        [4]<float>
    }


Define functions
==============================

.. code::

    [fun fun_name(args, ...)] {
        FLML sentences
    }

Example::

    [fun decode(arr)] {
        arr_decoded = [];
        for (ele in arr) {
            arr_decoded.append(ele ** 2 // 2 )
        }

        return arr_decoded;
    }


Modules
============================

.. code::

    [import module_name]

Example::

    [import math]
    [x = [1, 2, 3];
     y = [];
     for (ele in x){
        y.append(math.sin(ele));
      }
     ]


Comment
============================

Segment comment
---------------------------

A sentence whose '[...]' part start with '#', the sentence is
regard as a comment.

For example::
    [# this is a comment]<int>()

Line comment
------------------------

A line start with '//', the line is a comment.

For example::

    // [3]<int>

Block comment
-------------------------

Contents within '/*' and '*/' are regard as comments.

For example::

    /*
        [3]<int; float_num>
        [float_num]<float>
    */
