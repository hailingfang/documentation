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

```

    [1]<int32>(value="5"; name="besd type"; description="5 for dense")
    [1]<int32>(name="sample size"; NA="-9")
    [1]<int32; $esi_num>(name="number of esi")
    [1]<int32; $epi_num>(name="number of epi")
    [12]<int32>(value="-9";)
    [$epi_num; @indi_epi]{
        [1]{
            [$esi_num]<float>(name="beta value")
            [$esi_num]<float>(name="se value")
        }(belong="@indi_epi"; NA="-9")
    }(order="@indi_epi is ordered as epi file")

```

## sparse file formate | SMR_SPARSE_3 SPARSE_BELT

```
    [1]<int32>(value="3"; name="besd type"; description="3 for sparse file type")  
    [1]<int32>(name="sample size", NA="-9";)  
    [1]<int32>(name="esi number")  
    [1]<int32; $epi_num>(name="epi number")  
    [12]<int32>(value="-9")  
    [1]<uint64; =sigma(i = 1; i <= $epi_num; i++)($esi_num(@i))>(name="number of sparse beta se value")  
    [1]<uint64>(value="0")  
    [$epi_num; @indi_epi]{  
        {
            [1]<uint64; $beta_offset>(name="beta value offset of probe")
            [1]<uint64; $se_offset>(name="se value offset of probe")
        }(belong="@indi_epi") 
    }(orider="@indi_epi ordered as epi file")
    [$epi_num; @indi_epi]{  
        {
            [$beta_offset]<uint32>(name="esi index of beta";)
            [$se_offset]<uint32>(name="esi index of se";)
        }(belong="@indi_epi")
    }(belong="@indi_epi" order="epi file")
    [$epi_num; @indi_epi]{  
        {
            [$beta_offset]<float>(name="beta value")
            [$se_offset]<float>(name="se value")
        }(belong="@indi_epi")  
    }order="epi file")

```

## SMR_SPARSE_3F 0x40400000

```

    (define="$epi_number=length of epi file")
    [1]<int32>(name="file type", value="0x40400000")
    [1]<uint64; =sigma(i = 1; i <= $epi_number; i++>)(esi numb of $i)>(name="number beta or se value")
    [1]<uint64>(value="0", name="start beta se offset")
    [$epi_number; @indi_epi]{
        {[1]<uint64|$esi_num>(beta value offset of probe 1), [1]<uint64|$1>(se value offset of probe 1)}
        {[1]<uint64|$esi_num>(beta value offset of probe 2), [1]<uint64|$2>(se value offset of probe 2)}
        ...
    }
    [$epi number]{
        {[$1]<uint32>(beta esi file index of probe 1), [$1]<uint32>(se esi file index of probe 1)}
        {[$2]<uint32>(bete esi file index of probe 2), [$2]<uint32>(se esi file index of probe 2)}
        ...
    }
    [$epi number]{
        {[$1]<float>(beta value of probe 1), [$1]<float>(se value of probe 1)}
        {[$2]<float>(beta value of probe 2), [$2]<float>(se value of probe 2)}
        ...
    }

```
