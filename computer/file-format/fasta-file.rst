FASTA file
=================

.. code::

    [%info](dsp="fasta file"; filetype="plaintext"; encode="ascii")

    [$+] {
        [1] <string; =">.+"> (dsp="head line"; re="true"; end="\n")
        [$+] {
            [1] <string; ="[a-zA-Z-]+">
                (re="true"; value="for nucletide data, the value may be only characters of A, C, G, T,N, U";
                 end="\n")
        } (dsp="body lines")
    } 