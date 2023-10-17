GTF file
=============

GTF file FLML description


.. code::
    
    [%deflabel fieldname "the name of line fields"]
    [%info](dsp="gtf file"; filetype="plaintext"; encode="ascii")\
    [1]<string; ="#gtf-version 2.2">(dsp="gtf version line", re="^#gtf-version\s\d+\.\d+", end="\n")
    [$*] <string>(dsp="gtf information lines"; re="^#!.+")
    [$+] {
        [1] {
            [1] <string> (dsp="name of the chromosome or scaffold"; fieldname="seqname")
            [1] <string> (dsp="name of program that generated this feature"; filename="source")
            [1] <string; ={'CDS', 'gene', 'stop_codon', 'start_codon', 'exon', 'transcript'}>
                (dsp="feature type name"; fieldname="feature")
            [1] <string> (dsp="Start position* of the feature, with sequence numbering starting at 1"; datatype=int; fieldname="left")
            [1] <string> (dsp="End position* of the feature, with sequence numbering starting at 1"; datatype=int; fieldname="right")
            [1] <string> (datatype=float; fieldname="score")
            [1] <string; ={"-", "+"}> (fieldname="orientation")
            [1] <string; ={"0", "1", "2"}> (dsp=""; fieldname="frame")
            [1] {
                [$+] {
                    [1] <string> (dsp="one attribute", re='^.+\s".+";\s')
                } 
            } (dsp=""; fieldname="attribute")

        } (dsp="gtf information lines"; end="\n"; sep="\t")

    } (dsp="record lines")

    [1] <string; ="###"> (dsp="last line", end="\n")


Reference
---------------
https://pcingola.github.io/SnpEff/se_build_db_gff_gtf/
https://useast.ensembl.org/info/website/upload/gff.html
