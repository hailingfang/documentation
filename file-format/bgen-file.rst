BGEN format
================

version 1.2

.. code::

    [1] <uint32; :$offset_to_data> (dsp="offset to first data block")

    [1] <uint32; :$header_size> <dsp="size in byte of header block">
    [1] <uint32; :$vari_num> <dsp="variant number">
    [1] <uint32; :$sample_num> <dsp="sample number">
    [4] <char; =["b", "g", "e", "n"]> (dsp="megic number")
    [$header_size - 20] <byte> <dsp="free data area">
    
    [1] {
        [2] <bit; ={0, 1}> (dsp="flag for whether compressed"; value="0 for not compressed, 1 for compressed")
        [4] <bit; ={0, 1, 2}> (dsp="layout"; value="0: layout 0; 1: layout 1; 2: layout 2")
        [25] <bit> (dsp="not defined")
        [1] <bit; :$sample_flg> (dsp="indicate whether include sample indentifier data"; value="0: not included; 1: included")
    
    } (dsp="flags")


    [%if $sample_flg] {
        [1] <uint32> (dsp="size in byte of sample indentifier block")
        [1] <uint32; :$sample_num_2> (dsp="number of sample")
        [%assert $sample_num_2 == $sample_num]
        [$sample_num] {
            [1] <uint16; :$indentifier_string_len> (dsp="length of indentifier of one sample")
            [$indentifier_string_len] <char> (dsp="indentifier")
        
        } (dsp="sample data, the data is char, should interpreted as ascii")
    
    }


    [$vari_num] {
        [1] <uint32> ()

        [1] <uint16; :$len_vari_id> (dsp="length of variant identifier")
        [$len_vari_id] <char> (dsp="the variant identifier"; type="ascii")
        [1] <uint16; :$len_rsid> (dsp="legth of rsid")
        [$len_rsid]<char> (dsp="rsid"; type="ascii")
        [1] <uint16; :$len_chrom> (dsp="lenght of chromosome string")
        [$len_chrom] <char> (dsp="chromosome"; type="ascii")
        [1] <uint32> (dsp="the variant position")
        [1] <uint16; :$allel_num> (dsp="number of allels")
        [$allel_num] {
            [1] <uint32; :$allel_len> (dsp="length of allel string")
            [$allel_len] <char> (dsp="the allel string"; type="ascii")
    
        }

        [%if $layout == 1] {
            [%if compress_flg == 1] {
                [1] <uint32; :$compressed_len> (dsp="size of compressed genotype data, if $compress_flg is 0, this segment is ignored")
                [$compressed_len] <byte; :@compressed_dt> (dsp="genotype data which is compressed")
                [%let @genotype_dt = $zlib_decompress(@compressed_dt)]
                [%assert $arraylen(@genotype_dt) == 6 * $vari_num]
            }

            [%elif $compress_flg == 0] {
                [$vari_num * 6] <byte; :@genotype_dt> (dsp="genotype data")
            }
        
            [%parse @genotype_dt] {
            
                [$sample_num] {
                    [1] <uint16; :$pb1> (dsp="probability of homozygous of allel 1")
                    [1] <uint16; :$pb2> (dsp="probability of Heterozygous")
                    [1] <uint16; :$pb3> (dsp="probability of homozygous of allel 2")
                }

                [%let $pb1_converted = $convert_to_prob($pb1)]
                [%let $pb2_converted = $convert_to_prob($pb2)]
                [%let $pb2_converted = $convert_to_prob($pb3)]
            
            }
        }

        [%if $layout == 2] {
            [1] <uint32; $data_size> (dsp="the offset to the next variant block or end of file")
        
            [%if $compress_flg == 1] {
                [1] <uint32; :$decompressed_size> (dsp="size after decompress")
                [$data_size - 4] <byte; :@vair_data_compressed> (dsp="compressed data")
                [%let @vari_data_ori = $decompress_fuction(@vair_data_compressed)]
            }

            [%else] {
                [$data_size] <byte; :@vair_data_ori> (dsp="data which not compressed")
            }
        
            
            [%parse @vari_data_ori] {
            
                [1] <uint32> (dsp="number of individual")
                [1] <uint16> (dsp="number of allels")
                [1] <char> (dsp="minimum ploidy")
                [1] <char> (dsp="maximum ploidy")
                [$sample_num] <char> (dsp="ploidy of samples"; NA="most significant bit is 1")
                [1] <char> (dsp="denoted Phased indicating what is stored in the row")
                [1] <uint8> (dsp="number of bits used to store each probability in this row")
                [$?] <byte> ()
                //not finished yet
            
            }
        
        
        
        }
    
    }

    [%deffunc $convert_to_prob ($datain) $dataout] {
        [$dataout = $datain / 32768]
        [%return $dataout]

    } (dsp="fuction to convert 16 bits integer into a float to get probability")

    [%deffunc $convert_prob_to_int ($datain) $dataout] {

        [$dataout = $floor($datain * 32768)]
    
    } (dsp="convert probability into a 16 bits integer")  