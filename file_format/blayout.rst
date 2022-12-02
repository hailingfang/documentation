==========
blayout
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

    #Example:

    [1]<uint32>()
    [1]<uint32|$var1>()
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


Above is a example to use this language. the [], <>, (), {} is conserved as key as syntex.


1. [*Number*], The number of Unit 

    Content within [] is *Number* a number, a variable or a expression. To reprent the
    repeat of unit.

2. <*Unit*>, The *Unit*

    content within <> is Unit, can be bit, char, int, long, flaot, or int32, uint32 et al.
    The value of this Uint can be represented by a variable. For example, <int | $myvar>.

3. (*Describe*), The description of Unit

    Conten within (), is description of unit.

4. {*Group*}, Group the Unit

    To group a set of units as a unit. The to describe its repeat and meaning.


Example
++++++++++++++++++

Here are more example within this directory.