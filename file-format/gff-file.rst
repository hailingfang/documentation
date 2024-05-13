GFF file
==============

version gff3

.. code::

    [%info](dsp="gff file format"; filetype="plaintext"; encode="ascii")
    
    [1] <string; ="##gff-version 3"> (dsp="gff version line"; end="\n")
    [$*] {
        [1] <string; ="##.+"> (dsp="defination line"; re=$TRUE, end="\n")
    }

    [$+] {

        [1] {
            [1] <string> (dsp="seqname")
            [1] <string> (dsp="source"; NA=".")
            [1] <string> (dsp="feature")
            [1] <string> (dsp="start"; datatype="integer")
            [1] <string> (dsp="end"; datatype="integer")
            [1] <string> (dsp="score"; datatype="float"; NA=".")
            [1] <string; ={"+", "-"}> (dsp="strand")
            [1] <string; ={"0", "1", "2"}> 
                dsp="frame";
                NA=".";
                value={"0":"the first base of the feature is the first base of a codon",
                    "1": " the second base is the first base of a codon",
                    "2":" the second base is the second base of a codon"})
            [1] {

                [$*] {
                    [1] <string; ="[a-zA-Z]+[\-_0-9]*="> (dsp="attribute name"; re=$TRUE)
                    [1] <string; ='"[a-zA-Z]+";'> (dsp="attribute value"; re=$TRUE)
                }

            } (dsp="attribute")        
        } (dsp="one line of file"; sep=$TAB; end="\n")
    
    }
