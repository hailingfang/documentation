===============
Plink BED file
===============

The Plink BED file is used to store genotype data for individuals 
and must be accompanied by the .bim and .fam files. Both the .bim and .fam
files are plaintext files, with the .bim file containing variable information
and the .fam file containing individual information

.fam file
============

Fam file is a plaintext file without header line. and one line per sample with six fields.

.. code::

    [%info](dsp="fam file"; filetype="plaintext"; encode="ascii")

    [$+]{
        [1] <string; ="[a-zA-Z0-9]+")>(dsp="Family ID"; NA="0", re="true")
        [1] <string; ="[a-zA-Z0-9]+">(dsp="within family ID"; NA="0"; re="true")
        [1] <string; ="[a-zA-Z0-9]+">(dsp="Within family ID of father"; NA="0"; re="true")
        [1] <string; =re[a-zA-Z0-9]>(dsp="Within family ID of mother"; NA="0"; re="true")
        [1] <string; ={"1", "2", "0"}>(dsp="sex code"; value="'1' for male, '2' for female, '0' for unknown"; NA="'0'", datatype=int)
        [1] <string; ={"1", "2", "0", "-9"}>
            (dsp="phenotype value"; value="1 for control, 2 for case, -9 or 0 for missing"; NA="'-9' or '0'"; datatype=int)

        [1]<char; ='\n'>
    }(dsp="fam file field fixed plaintext file, it have no head line, every line have six field sperated by white character"; sep="$TAB")


.bim file
=================

Extended variant information file accompanying a .bed binary genotype table. have no
header line, and each line contain six fields.

.. code::

    [%info](dsp="bim file"; filetype="plaintext"; encode="ascii")

    [$linenum]{
        [$?]<string>(dsp="chromosome code", value="is a integer or X, Y, MT or 0, 0 for unknown", NA="0")
        [$?]<string>(dsp="a tring used as a variant identifier")
        [$?]<string>(dsp="position in morgans or centimorgans", datatype="a float, 0 for unknown", NA="0")
        [$?]<string>(dsp="base pair position", datatype="integer, 0 for unknown", NA="0")
        [$?]<string>(dsp="allele 1")
        [$?]<string>(dsp="allele 2")
        
        [1]<char; ='\n'>(dsp="new line")
    }(dsp="bim file has no head line, and every line has six field sperated by white space"; spe="$TAB")


.bed file
==============

.. code::

    [%info "bed binary file"]<>()
    [%file $famfile]<>(file="fam file")
    [%file $bimfile]<>(file="bim file")
    [%let $famfile_len = $filelen($famfile)]<>()
    [%let $bimfile_len = $filelen($bimfile)]<>()
    [%let $data_len_per_vari = $ceil(famfile_len / 4)]<>(dsp="variant data of 
        every four individuals was stored by one byte. if the $famfile_len
        can not be divided by four,  the remainder stored using a whole byte.")
    [3]<char; =[0x6c, 0x1b, 0x01]>(dsp="magic number, in lasted plink version, them should be 0x6c, 0x1b, 0x01")
    [$bimfile_len]{
        [$data_len_per_vari; ~$i]{
            [1]{
                [2]<bit>(dsp="low 7-8 bits of individual 4 * $i + 3")
                [2]<bit>(dsp="low 5-6 bits of individual 4 * $i + 2")
                [2]<bit>(dsp="low 3-4 bits of individual 4 * $i + 1")
                [2]<bit>(dsp="low 1-2 bits of individual 4 * $i")
            }(dsp="genotype of 4 individuals, store by 4 2-bits block"; value="00: Homozygous of first allele in .bim file. 10: Heterozygous. 11: Homozygous of second allele in .bim file. 01: Missing";)
        }(dsp="genotype data of one snp/variant, if individual number can not divided by 4, use a whole byte for remainder， use 0 for superfluous bits", order="$famfile")
    }(order="$bimfile")


Individuals order across byte
=================================

.. image:: ./imgs/plink_bed_file.svg


Meaning of bits
=====================

::

    Every of 2 bits of a byte for genotype.  
    * 00: Homozygous of first allele in .bim file.
    * 10: Heterozygous.
    * 11: Homozygous of second allele in .bim file.
    * 01: Missing

If N is not divisible by four, the extra high-order bits in the last byte of each block are always zero.


References
===============

https://www.cog-genomics.org/plink/1.9/formats#fam

`bed file <https://www.cog-genomics.org/plink/1.9/formats>`_

`plink2R <https://github.com/gabraham/plink2R/blob/master/plink2R/src/data.cpp>`_


