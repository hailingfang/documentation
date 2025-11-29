zlib bytes stream
======================

FLML description
--------------------

 ZLIB Compressed Data Format Specification version 3.3

.. code::

    [%file](dsp="zlib bytes stream", filetype="stream")

    [1] {
        [4] <bit; $cm>
            (dsp="compress method"; id="CM";
             value-dsp="8 for deflate compression method, 15 is conserved, values except 8 and 15 is not described in the RCF")

        [%if ($cm == 8)] {
            [4] <bit; $cinfo; =[0, 7]> (dsp="compression information"; value="windows_size = 2 ** ($cinfo + 8)"; id="CINFO")
        }
        [%else] {
            [4] <bit; =[0, 7]> (dsp="compression information"; id="CINFO")
        }
    } (dsp="Compression Method and flags")

    [1] {
        [5] <bit> (dsp="check bits for CMF and FLG")
        [1] <bit; $dic> (dsp="preset dictionary")
        [%if $cm == 8] {
            [2] <bit; ={0, 1, 2, 3}>
                (dsp="compression level";
                 value={0: "fastest algorithm", 1: "fast algorithm", 2: "default algorithm", 3: "maximum compression, slowest algorithm"})
        }
        [%else] {
            [2] <bit> (dsp="compression level")
        }


    } (dsp="flags"; id="FLG")

    [%if $dic] {


    }

    [%if $cm == 8] {


    }
    [%else] {
        [$+] <byte> (dsp="compressed data")
    }

    [$+] <byte> (dsp="Adler-32 checksum, a checksum value of the uncompressed data")



References
-----------------

`RCF 1950 <https://datatracker.ietf.org/doc/html/rfc1950>`_
