# BGEN file format


## version 1.2

```
[]<>(info="BGEN file format, version 1.2")

[1]<uint32; $first_block_offset>(dsp="offset from 5th bytes 
    of file, to the begin of first variant block")

[#head block]<>()
[1]{
    [1]<uint32; $head_len>(dsp="length of header block")
    [1]<uint32; $variant_num>(dsp="num of variant block")
    [1]<uint32; $sample_num_1>(dsp="sample number")
    [4]<char; = {['b', 'g', 'e', 'n'], [0, 0, 0, 0]}>(dsp="megic number, can be 
        'b', 'g', 'e', 'n' or 4 zero")
    [$head_len - 20]<char>(dsp="free data area")
    [1]{
        [2]<bits; = {0, 1}; $compress_flag>(dsp="0-1 bits, CompressedSNPBlocks"; value="[%note 1]<>()")
        [4]<bits; = {0, 1, 2}; $layout>(dsp="layout"; value="0: layout 0. 1: layout 1. 2: layout 2")
        [25]<bits>(dsp="not used")
        [1]<bits; = {0, 1}; $sample_flag>(dsp="sample identifiers"; value="0: indicates sample identifiers are not stored.
            1: Indicates a sample identiﬁer block follows the header.")
    }(dsp="flags")
}(id="head block"; dsp="contains global information about the file")

[#sample block]<>()
[%if $sample_flag == 1]{
    [1]<uint32; $sample_block_size>(dsp="length in bytes of the sample identiﬁer block")
    [1]<uint32; $sample_num>(dsp="sample number")
    [%assert $sample_num == $sample_num_1]<>()
    [%let $sample_id_size_total = 0]<>()
    [$sample_num]{
        [1]<uint16; $len_sample_id; +$sample_id_size_total>(dsp="length of sample identifier")
        [$len_sample_id]<char>(dsp="sample id")
    }(dsp="sample information")
    [%assert $sample_bloc_size = 8 + 2 * $sample_num + $sample_id_size_total]<>()
}(dsp="a sample block would include if sample flag is 1")

[#variant block]<>()
[$variant_num]{
    [%if $layout == 1]{
        [1]<uint32>(dsp="The number of individuals the row represents")
    }()
    [1]<uint16; $len_variant_id>(dsp="length of variant id")
    [$len_variant_id]<char>(dsp="variant identifier")
    [1]<uint16; $len_rsid>(dsp="rsid string length")
    [$len_rsid]<char>(dsp="rsid")
    [1]<uint16; $len_chr>(dsp="chromosome string length")
    [$len_chr]<char>(dsp="chromosome")
    [1]<uint32>(dsp="variant position")
    [%if $layout == 1]{
        [1]<uint16; = 2; $allel_num>(dsp="allel number")
    }()
    [%else]{
        [1]<uint16; $allel_num>(dsp="allel number")
    }()
    [$allel_num]{
        [1]<uint32; $allel_len>()
        [$allel_len]<char>(dsp="allel")
    }()

    [%if $layout == 0]{
        [%mesg "layout 0 is depreyted"]<>()
    }()
    [%elif $layout == 1]{
  
        [%if $compress_flag == 0]{
            [6 * $sample_num]<byte>()
        }()
        [%else]{
            [1]<uint32; $snp_block_size>()
            [$snp_block_size]<byte>()
            [%mesg "size of after uncompression should be 6 * $sample_num"]<>()
        }()
    }
    [%elif $layout == 2]{
        [1]<uint32; $snp_block_size>(dsp="totall size of data of this variant")
        [%if compress_flag == 0]{
            [%extend $block_layout1]{
                [$snp_block_size]<byte>()
            }()
        }()
        [%else]{
            [1]<uint32>(dsp="probability data size after uncompression")
            [%extend $block_layout2]{
                [$snp_block_size - 4]<byte>()
            }()
        }()
    }
    [%else]{
        [%error "layout not recgnized"]<>()
    }()
}()

[%block $block_layout1]{

}()

[%block $block_layout2]{

}()


[%note 1]<
    0: Indicates SNP block probability data is not compressed
    1: Indicates SNP block probability data is compressed using zlib's compress() function.
>()

```

## Reference

[bgen version 1.2](https://www.well.ox.ac.uk/~gav/bgen_format/spec/v1.2.html)

[bgen lastest version](https://www.well.ox.ac.uk/~gav/bgen_format/spec/latest.html)

## Notes



