There kinds of file format of besd file. First is Dense file type, and second is sparse file type.
## Macros
### Dense
`#define DENSE_FULL 0`

`#define DENSE_BELT 1`

`#define OSCA_DENSE_1 4 // 0x00000004: RESERVEDUNITS*ints  + floats  :  <beta, se> for each SNP across all the probes are adjacent.`

`#define SMR_DENSE_1 0 // 0x00000000 + floats  : beta values (followed by se values) for each probe across all the snps are adjacent.`

`#define SMR_DENSE_3 5  // RESERVEDUNITS*ints + floats (indicator+samplesize+snpnumber+probenumber+ 12*-9s + values) [SMR default and OSCA default]`

### Sparse
`#define SPARSE_FULL 2`

`#define SPARSE_BELT 3`

`#define OSCA_SPARSE_1 1 // 0x00000001: RESERVEDUNITS*ints + uint64_t  + uint64_ts + uint32_ts + floats: value number + (half uint64_ts and half uint32_ts of SMR_SPARSE_3) [OSCA default]`

`#define SMR_SPARSE_3F 0x40400000 // 0x40400000: uint32_t + uint64_t + uint64_ts + uint32_ts + floats`

`#define SMR_SPARSE_3 3 // RESERVEDUNITS*ints + uint64_t + uint64_ts + uint32_ts + floats (indicator+samplesize+snpnumber+probenumber+ 6*-9s +valnumber+cols+rowids+betases) [SMR default]`


## dense file format | SMR_DENSE_3
    [1]<int32>(file type, 5 for dense file type;)
    [1]<int32>(sample sile, -9 for NA;)
    [1]<int32 | $esi_num>(esi number;)
    [1]<int32 | $epi_num>(epi number;)
    [12]<int32>(value is -9;)
    [$epi_num]{
        [1]{
            [$esi_num]<float>(beta value, -9 for NA;)
            [$esi_num]<float>(se value, -9 for NA;);
        }(beta value and se vaule of same probe;)
    }(the order if same consistent with epi file;)


## sparse file formate | SMR_SPARSE_3 SPARSE_BELT
    [1]<int32>(file type, 3 for sparse file type;)  
    [1]<int32>(sample size, -9 for NA;)  
    [1]<int32>(number of esi;)  
    [1]<int32 | $epi_num>(number of probe;)  
    [12]<int32>(value is -9;)  
    [1]<uint64>(number of sparse beta se value;)  
    [1]<uint64>(value is 0;)  
    [$epi_num]{  
        [1]{
            [1]<uint64|$beta_offset>(beta value offset of probe;)
            [1]<uint64|$se_offset>(se value offset of probe;)
        }(offset of beta se, $beta_offset should equal to $se_offset;) 
    }()
    [$epi_num]{  
        {
            [$beta_offset]<uint32>(beta corresponding snp/esi index of probe 1;)
            [$se_offset]<uint32>(se corresponding snp/esi index of probe 1;)
        }  
    }()  
    [$epi_num]{  
        {
            [$beta_offset]<float>(beta value of probe 1;)
            [$se_offset]<float>(se value of probe 1;)
        }  
    }()

## SMR_SPARSE_3F 0x40400000
    [1]<int32>(file type, value is 0x40400000)
    [1]<uint64>(number of sparse beta se value)
    [1]<uint64>(value is 0, start beta se offset)
    ["epi number"]{
        {[1]<uint64|$1>(beta value offset of probe 1), [1]<uint64|$1>(se value offset of probe 1)}
        {[1]<uint64|$2>(beta value offset of probe 2), [1]<uint64|$2>(se value offset of probe 2)}
        ...
    }
    ["epi number"]{
        {[$1]<uint32>(beta esi file index of probe 1), [$1]<uint32>(se esi file index of probe 1)}
        {[$2]<uint32>(bete esi file index of probe 2), [$2]<uint32>(se esi file index of probe 2)}
        ...
    }
    ["epi number"]{
        {[$1]<float>(beta value of probe 1), [$1]<float>(se value of probe 1)}
        {[$2]<float>(beta value of probe 2), [$2]<float>(se value of probe 2)}
        ...
    }


