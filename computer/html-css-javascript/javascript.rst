JavaScript
==================

Varibles
-------------------

.. code:: javascript

   var x = 1;
   let y = 2;
   const z = 3;


Datatypes
-----------------

.. code:: javascript

   let x;
   x = 123;
   x = "hello world";
   //Array
   x = ["aa", "bb", 123];
   //Object
   x = {"aa": 12, bb: "hhh", 33: "aaa"};
   //RegExp
   x = /^A.+/;


Conditionals
-------------------

.. code:: javascript

   if (condition1) {
      statement1;
    } else if (condition2) {
      statement2;
    } else if (conditionN) {
      statementN;
    } else {
      statementLast;
    }


    switch (expression) {
      case label1:
        statements1;
        break;
      case label2:
        statements2;
        break;
      // …
      default:
        statementsDefault;
    }

Loops
------------------

.. code:: javascript

   for (initialization; condition; afterthought)
      statement

    while (condition)
        statement

    for (variable in object)
      statement

    for (variable of iterable)
      statement


Functions
------------------

.. code:: javascript

    function FunName(Args) {
      statement
    }


    const square = function (number) {
      return number * number;
    };

    const factorial = function fac(n) {
      return n < 2 ? 1 : n * fac(n - 1);
    };

    //Immediately Invoked Function Expressions (IIFE)
    (function (name){console.log("hello world.");})();


DOM
--------------------



References
--------------------

https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/
