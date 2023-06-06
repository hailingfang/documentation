===================
GCTA BESD file
===================

The BESD file is a binary file format used in GCTA, OSCA, and SMR to store 
GWAS analysis results. It must be accompanied by the .epi and .esi files when used.

.epi file
================

The .epi file is a plaintext file where every line represents an entry of
information for a phenotype. Therefore, the number of lines in the .epi file is
equal to the number of phenotypes.

.. code::

    [%info ".epi plaintext file"]<>()
    [%file $epi_file]<>(file="epi file")
    [%let $epi_num = $filelen($epi_file)]<>(dsp="phenotypes number")
    [$epi_num]{
        [$?]<ascii>(dsp="chromosome number", type="string", value="number or X, Y, MT and so on")
        <1><ascii; =$white_space>(dsp="a $white_space used to seprat fields")
        [$?]<ascii>(dsp="variant ID", type="string")
        [1]<ascii; =$white_space>()
        [$?]<ascii>(dsp="physical position", type="float")
        [1]<ascii; =$white_space>()
        [$?]<ascii>(dsp="base position", type="int")
        [$?]<ascii>(dsp="orientation", value="+ or -")
        [1]<ascii; ="\n">()
    }()

.esi file
==============

.esi file is used to record information of variants.

.. code::

    [%file $esi_file]<>(file="esi file")
    [%let $esi_num = $filelen($esi_file)]<>()
    [$esi_num]{
        [1]<int>(dsp="chromosome")
        [1]<string>(dsp="rsid")
        [1]<float>(dsp="physical position")
        [1]<uint32>(dsp="base position")
        [1]<string>(dsp="reference allel")
        [1]<string>(dsp="alternertive allel")
        [1]<float>(dsp="minor allel frequency")

    }()


.besd file
=================

There kinds of file format of besd file. First is Dense file type, and second is sparse file type.

Macros
------------------

Defined C macros for besd file format. 

* Dense
    ::

        #define DENSE_FULL 0
        #define DENSE_BELT 1
        #define OSCA_DENSE_1 4 // 0x00000004: RESERVEDUNITS*ints  + floats  :  <beta, se> for each SNP across all the probes are adjacent.
        #define SMR_DENSE_1 0 // 0x00000000 + floats  : beta values (followed by se values) for each probe across all the snps are adjacent.
        #define SMR_DENSE_3 5  // RESERVEDUNITS*ints + floats (indicator+samplesize+snpnumber+probenumber+ 12*-9s + values) [SMR default and OSCA default]

* Sparse
    ::

        #define SPARSE_FULL 2
        #define SPARSE_BELT 3
        #define OSCA_SPARSE_1 1 // 0x00000001: RESERVEDUNITS*ints + uint64_t  + uint64_ts + uint32_ts + floats: value number + (half uint64_ts and half uint32_ts of SMR_SPARSE_3) [OSCA default]
        #define SMR_SPARSE_3F 0x40400000 // 0x40400000: uint32_t + uint64_t + uint64_ts + uint32_ts + floats
        #define SMR_SPARSE_3 3 // RESERVEDUNITS*ints + uint64_t + uint64_ts + uint32_ts + floats (indicator+samplesize+snpnumber+probenumber+ 6*-9s +valnumber+cols+rowids+betases) [SMR default]

sparse and dense file formate | SMR_SPARSE_3 SPARSE_BELT & SMR_DENSE_3
=========================================================================

.. code::

    [%fileinfo] <> (dsp="besd file", endianness="little", filetype="binary")
    [%linkfile $epi_file] <> (dsp="a epi file, record phenotype information", filetype="text")
    [%let $epi_len = $filelen($epi_file)] <>()
    [%let @epi_order = $getorder($epi_file)] <> ()
    [%linkfile $esi_file] <> (dsp="a esi file, record variants information", filetype="text")
    [%let $esi_len = $filelen($esi_file)] <> ()
    [%let @esi_order = $getorder($esi_file)] <> ()
    [1] <int32; :=$file_format> (dsp="besd type",value="{3: sparse},{5: dense}")
    [1] <int32> (dsp="sample number", NA="-9")
    [1] <int32; :$esi_num> (dsp="variant number")
    [%assert $esi_num == $esi_len] <> ()
    [1] <int32; :$epi_num> (dsp="phenotype number")
    [%assert $epi_num == $epi_len] <> ()
    [12] <int32; =-9> (dsp="keeped for future use";)
    
    [%if $file_format == 5] {
        [$epi_num; ~$epi_inter_num] {
            [$esi_num] <float> (dsp="bata of one phenotype", relatedto="@epi_order[$epi_inter_num]", alignwith="$esi_order")
            [$esi_num] <float> (dsp="se of one phenotype", relatedto="@epi_inter_num[$epi_inter_num]", alignwith="$esi_order")
        }(dsp="data for all phenotype", dspelement="beta and se data of one phenotype", alignwith="@epi_order")
    }(dsp="file format is dense")
    
    [%elif $file_format == 3] {
        [%let $value_sum = 0] <> (dsp="sum of couter of value")
        [1] <uint64; =:$value_sum> ()
        [1] <uint64; =0; :@index_array_offset> (dsp="the first value of variants index offset")
        [$epi_num; ~$epi_it] {
            [%let $offset_block] <> (dsp="a value represents the block size of beta or se of this phenotype")
            [1] <uint64; =@index_array_offset[-1] + $offset_block; :@index_array_offset; :+$value_sum> (relatedto="@epi_order[$epi_it]")
            [1] <uint64; =@index_array_offset[-1] + $offset_block; :@index_array_offset; :+$value_sum> (relatedto="@epi_order[$epi_it]")
        }(dsp="index offset length array", alignwith"@epi_order")
        [%assert @index_array_offset[-1] == value_sum] <> ()
        [%let @index_array_collector = []] <> ()
        [$epi_num; ~$epi_it] {
            [%let @beta_offsets = []] <> ()
            [%let @se_offsets = []] <> ()
            [@index_array_offset[2 * $epi_it + 1] - @index_array_offset[2 * $epi_it]]<uint32; :@beta_offsets>()
            [@index_array_offset[2 * $epi_it + 2] - @index_array_offset[2 * $epi_it + 2]]<uint32; :@se_offsets>()
            [$append(@index_array_collector, @beta_offsets)] <> ()
            [$append(@index_array_collector, @se_offsets)] <> ()
        }()
        [$epi_num; $epi_it]{
            [@index_array_offset[2 * $epi_it + 1] - @index_array_offset[2 * $epi_it]] <float> (alignwith="@index_array_collector[$epi_it * 2]")
            [@index_array_offset[2 * $epi_it + 2] - @index_array_offset[2 * $epi_it + 2]] <float> (alignwith="@index_array_collector[$epi_it * 2 + 1]")
        }
    }(dsp="file format is sparse")
    
    [%else] {
        [%error]<>(mesg="the format is not recognized")
    }()


SMR_SPARSE_3F 0x40400000
==============================

.. code::

    [# "need correct"]<>()
    []<>(%defvalue $epi_num "length of epi file")
    [1]<int32>(dsp="file type"; value="0x40400000")
    [1]<uint64; $value_num; $value_num = 0;  for(i = 1; i <= $epi_numr; i++>)($value_num += $beta_offset + $se_offset)>(dsp="number beta or se value")
    [1]<uint64>(dsp="start beta se offset"; value="0")
    [$epi_num; @]{
        [1]<uint64; @epi_num.$beta_offset>(offset of beta value)
        [1]<uint64; @epi_num.$se_offset>(offset of se value)
    }(dsp="offset length or number of beta and se of each probe"; order="epi file")
    [$epi num; @]{
        {[$1]<uint32>(beta esi file index of probe 1), [$1]<uint32>(se esi file index of probe 1)}
        {[$2]<uint32>(bete esi file index of probe 2), [$2]<uint32>(se esi file index of probe 2)}
        ...
    }
    [$epi num; @]{
        {[$1]<float>(beta value of probe 1), [$1]<float>(se value of probe 1)}
        {[$2]<float>(beta value of probe 2), [$2]<float>(se value of probe 2)}
        ...
    }


