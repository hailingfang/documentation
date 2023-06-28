GCTA BESD file
===================

The BESD file is a binary file format used in GCTA, OSCA, and SMR to store 
GWAS analysis results. It must be accompanied by the .epi and .esi files when used.




.epi file
-------------------

The .epi file is a plaintext file where every line represents an entry of
information for a phenotype. Therefore, the number of lines in the .epi file is
equal to the number of phenotypes.

FLML description
++++++++++++++++++++++++

.. code::

    [%file]"](dsp="epi file"; filetype="plaintext"; encode="ascii"; role="main")

    [$+]{
        [1]<string; ="[0-9XYMT]+">(dsp="chromosome number", type="string", value-dsp="number or X, Y, MT and so on"; re=$TRUE)
        [1]<string; ="[0-9a-zA-Z_]+">(dsp="variant ID", datatype="string"; re=$TRUE)
        [1]<string>(dsp="physical position", datatype="float")
        [1]<string>(dsp="base position", datatype="int")
        [1]<string>(dsp="orientation", value-dsp="+ or -")
        
        [1]<char; ='\n'>
    }(sep=$WHITESPACE)




.esi file
-----------------

.esi file is used to record information of variants.

FLML description
+++++++++++++++++++++

.. code::

    [%file]<>(dsp="esi file"; filetype="plaintext"; encode="ascii"; role="main")

    [$+]{
        [1]<string>(dsp="chromosome"; value-dsp="a number, X, Y or MT and so on")
        [1]<string>(dsp="rsid")
        [1]<string>(dsp="physical position"; datatype="float")
        [1]<string>(dsp="base position"; datatype="unsigned integer")
        [1]<string>(dsp="reference allel")
        [1]<string>(dsp="alternertive allel")
        [1]<string>(dsp="minor allel frequency"; datatype="float")

        [1] <char; ='\n')
    }(sep=$WHITESPACE)



.besd file
-----------------------

There kinds of file format of besd file. First is Dense file type, and second is sparse file type.

Macros
++++++++++++++

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
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code::

    [%file] (dsp="besd file", endianness="little", filetype="binary"; role="main")
    [%let $epi_fname = @CMDARGS[1]]
    [%let $esi_fname = @CMDARGS[2]]
    [%file $epi_file $epi_fname] (dsp="epi file"; filetype="plaintext"; role="company")
    [%file $esi_file $esi_fname] (dsp="esi file"; filetype="plaintext"; role="company")

    [%let $epi_len = $filelinenum($epi_file)]
    [%let $esi_len = $filelinenum($esi_file)]
    [%let @epiorder = $getorder($epi_file)]
    [%let @esiorder = $getorder($esi_file)]

    [1] <int32; $file_format; ={3, 5}> (dsp="besd file format"; value={3: "sparse", 5: "dense"})
    [1] <int32> (dsp="sample number"; NA=-9)
    [1] <int32; $esi_num> (dsp="number of variants")
    [%assert $esi_num == $esi_len]
    [1] <int32; $epi_num> (dsp="number of probe")
    [%assert $epi_num == $epi_len]
    [12] <int32; =-9> (dsp="conserved for future use")

    [%if $file_format == 5] {

        [$epi_num] {
            [$esi_num] <float> (dsp="beta values of a probe"; alignwith=@esiorder)
            [$esi_num] <float> (dsp="se values of a probe"; alignwith=@esiorder)        
        } (alignwith@epiorder)
    
    
    } (dsp="data stored using dense format")


    [%if $file_format == 3] {
    
        [%let $value_num_count = 0]
        [1] <uint64; =:$value_num_count> (dsp="the number of values, include beta and se")
        [%let @offsets = []]
        [1] <uint64; =0; :@offsets> (dsp="frist value of offset")

        [$epi_num] {
            [1] <uint64; $offset_beta> (dsp="totall offset of beta data")
            [%let $beta_dt_len = $offset_beta - @offsets[-1]](dsp="this is the beta data number of this probe")
            [$append(@offsets, $offset_beta)]
            [$value_num_count += $beta_dt_len]
            [1] <uint64; $offset_se> (dsp="total offset of se data")
            [%let $se_dt_len = $offset_se - @offsets[-1]] (dsp="se data number")
            [$append(@offsets, $offset_se)]
            [$value_num_count += $se_dt_len]
            [%assert $beta_dt_len == $se_dt_len]
        } (dsp="data offset of each probe"; alignwith=@epiorder)
        [%assert $value_num_count == @offsets[-1]]

        [%let @all_index_order]
        [$epi_num; ~$i] {
            [@offsets[$i * 2 + 1] - @offsets[$i * 2]; ^@beta_order]     <uint32; @beta_index> (dsp="index of beta"; value-alignwith=@esiorder)
            [@offsets[$i * 2 + 2] - @offsets[$i + 2 + 1]; ^@se_order]   <uint32; @se_index> (dsp="index of se"; value-alignwith=@esiorder)
            [$append(@all_index_order, @beta_order); $append(@all_index_order, @se_order)]
        } (dsp="beta and se data indexs"; alignwith=@epiorder)

        [$epi_num; ~$j] {
            [@offsets[$i * 2 + 1] - @offsets[$i * 2]]     <float> (dsp="beta values of this probe"; alignwith=@all_index_order[$j * 2])
            [@offsets[$i * 2 + 2] - @offsets[$i + 2 + 1]] <float> (dsp="se values of this probe"; alignwith=@all_index_order[$j * 2 + 1])
        
        } (dsp="beta and se data blocks")


    } (dsp="data stored using sparse format")

    [%else] {
    
        [%error "file format not recognized"]
    }




.. 
    SMR_SPARSE_3F 0x40400000
    +++++++++++++++++++++++++++++++

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




BESD version 2
----------------------

This is a new version may adepted in future

.. code::

    [%file](dsp="besd file version 2"; endianness="little"; filetype="binary"; role="main")

    [4] <char; =["b", "e", "s", "d"]> (dsp="besd magic number")
    [1] <uint32> (dsp="BESD file format version")

    [32] <byte> (dsp="store sha256 sum of following data")
    [1] <char; ={13, 14}; $file_type> (dsp="besd file type"; value="13 for new sparse version, 14 for new dense version")
    [1] <uint64; $probe_num> (dsp="probe number")
    [1] <uint64; $vari_num> (dsp="variants number")
    [1] <uint64> (dsp="individual number"; NA=0)


    [1] {
        [1] <bit; $probeinfo_flg> (dsp="flag for probe information"; value="0 for probe information not stored by this file, 1 stored")
        [1] <bit; $variantinfo_flg> (dsp="flag for vairant information"; value="0 for variants information is not stored, 1 stored")
        [2] <bit; $compress_flg> (dsp="flag for compression"; value="0 for not compressed, 1 for zlib compressed, other value is rested for future")
        [4] <bit; =[0, 0, 0, 0]> (dsp="conserved")
    } (dsp="flags")


    [%if probeinfo_flg == 1] {
        [$probe_num; ^@probe_order] {
            [5]<uint16; :@probe_str_len> (dsp="the length of probe information in char")
            [@probe_str_len] <char> (dsp="information string of probe")
        }
    }
    [%else] {
        [%file $probe_file "probe text file"]
        [%let $probe_file_len = $getlinelen($probe_file)]
        [%assert $probe_file_len == $probe_num]
        [%let @probe_order = $getorder($probe_file)]
    }


    [%if variantinfo_flg == 1] {
        [$vari_num; ^@vair_order] {
            [7] <uint16; :@vari_str_len> (dsp="the length of eahc field")
            [@vari_str_len] <char> (dsp="vairant information")
        }
    }
    [%else] {
        [%file $variant_file "variant information file"]
        [%let $variant_file_len = $getlinelen($variant_file)]
        [%assert $variant_file_len == $vari_num]
        [%let @vair_order = $getorder($variant_file)]
    }


    [%if file_type == 13] {

        [%if $compress_flg == 0] {
            [$probe_num] {
                [1] <uint32; :$vari_num_each> (dsp="vairant number of this probe")
                [$vari_num_each] <uint32> (dsp="index of vairatn", alignwith="vair_order")
                [$vari_num_each] <float> (dsp="beta data")
                [$vari_num_each] <float> (dsp="se data")
            }
        }
        
        [%else] {
            [$probe_num] {
                
                [1] <uint32; :$vari_num_probe> (dsp="variant number of this probe")
                [1] <uint32; :$data_size_probe> (dsp="data size of this probe")
                [%let $actual_vari_num_probe = 0]
                [%let $actual_size_probe = 0]
                [$?] {
                    [1] {
                        [1] <uint16; :$vari_num_block; :+$actual_vari_num_probe> (dsp="vairant number of this block")
                        [1] <uint16; :$compressed_len> (dsp="data size in byte compressed")
                        [1] <uint16> (dsp="data size in byte decompressed")
                        [$compressed_len] <byte; :@compressed_data> (dsp="compressed data")
                        [$actual_size_probe += 6 + $compressed_len]
                        [%let @decompressed_data = $decompress_fuction($compressed_data)]
                        [%parse @decompressed_data] {
                            [$vari_num_block] <int> (dsp="variant index of this block", alignwith="@vair_order")
                            [$vari_num_block] <float> (dsp="beta data of this block")
                            [$vari_num_block] <float> (dsp="se data of this block")
                        }

                        [%assert $actual_vari_num_probe == $vari_num_probe]
                        [%assert $actual_size_probe == $data_size_probe]
                    }
                }
            
            } (dsp="beta se data"; alignwith="@probe_order")
        }
    }


    [%if file_format == 14] {

        [%if $compress_flg == 0] {
            [$probe_num] {
                [$vari_num] <float> (dsp="beta data", alignwith="@vair_order")
                [$vari_num] <float> (dsp="se data", alignwith="@vair_order")
            
            } (dsp="probe beta and se data", alignwith="@probe_order")
        }

        [%else] {
            [$probe_num] {
                [1] <uint32; :$each_probe_data_len> (dsp="beta, se data storage length of one probe") 
                [%let $acture_len = 0]
                [%let $acture_vari_num = 0]
                [$?] {
                    [1] <uint16; :+acture_vari_num; :$vari_num_block> (dsp="contained variant number of this compressed block")
                    [1] <uint16; :$compressed_len> (dsp="size in byte after compressed")
                    [1] <uint16> (dsp="size in byte decompressed")
                    [$acture_len += 6 + $compressed_len]
                    [$compressed_len] <byte; :@compressed_data> (dsp="compressed data")

                    [%let @decompressed_data = $decompress_fuction(@compressed_data)] <> (dsp="decompress the data")
                    [%parse @decompressed_data] {
                        [$vari_num_block] <float> (dsp="beta data")
                        [$vari_num_block] <float> (dsp="se data")
                    } (dsp="the layout of decompressed data")

                } (alignwith="@vair_order")

                [%assert $acture_len == $each_probe_data_len]
                [%assert $acture_vari_num == $value_num]
                
            } (dsp="beta and se data"; alignwith="@probe_order")
        }
    }






