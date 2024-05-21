SAM file
=================

version 1.6

.. code::

    [%info "sam plaintext file"]<>(filetype="plaintext"; code="ascii")

    [$?] {
        [1] <string; ="@HD"> (dsp="head line")
        [1] <string; ="VN:[0-9]+\.[0-9]+"> (dps=""; re="true")
        [$?] {
            [1] <string; ="SO:"> ()
            [1] <string; = {"unknow", "unsorted", "queryname", "coordinate"}; :$so_value> ()
        } (dsp="")
        [$?] <string; ="GO:" + {"none", "query", "Reference"}>
        (dsp="")

        [$?] <string; ="SS:" + $so_value + ":" + $sub_order> ()

        [1] <char; ="\n">

    } (dsp="head line for version", sep="$TAB")
