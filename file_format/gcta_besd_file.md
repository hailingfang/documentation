# GCTA BESD file

## .epi file

## .esi file

## .besd file


There kinds of file format of besd file. First is Dense file type, and second is sparse file type.
### Macros

Defined C macros for besd file format. 

#### Dense
`#define DENSE_FULL 0`

`#define DENSE_BELT 1`

`#define OSCA_DENSE_1 4 // 0x00000004: RESERVEDUNITS*ints  + floats  :  <beta, se> for each SNP across all the probes are adjacent.`

`#define SMR_DENSE_1 0 // 0x00000000 + floats  : beta values (followed by se values) for each probe across all the snps are adjacent.`

`#define SMR_DENSE_3 5  // RESERVEDUNITS*ints + floats (indicator+samplesize+snpnumber+probenumber+ 12*-9s + values) [SMR default and OSCA default]`

#### Sparse
`#define SPARSE_FULL 2`

`#define SPARSE_BELT 3`

`#define OSCA_SPARSE_1 1 // 0x00000001: RESERVEDUNITS*ints + uint64_t  + uint64_ts + uint32_ts + floats: value number + (half uint64_ts and half uint32_ts of SMR_SPARSE_3) [OSCA default]`

`#define SMR_SPARSE_3F 0x40400000 // 0x40400000: uint32_t + uint64_t + uint64_ts + uint32_ts + floats`

`#define SMR_SPARSE_3 3 // RESERVEDUNITS*ints + uint64_t + uint64_ts + uint32_ts + floats (indicator+samplesize+snpnumber+probenumber+ 6*-9s +valnumber+cols+rowids+betases) [SMR default]`


#### dense file format | SMR_DENSE_3

```

    [1]<int32>(dsp="besd file format"; value="5 for SMR_DENSE_3 dense format")
    [1]<int32>(dsp="sample size"; value="-9 for NA")
    [1]<int32; $esi_num>(dsp="number of esi")
    [1]<int32; $epi_num>(dsp="number of epi")
    [12]<int32>(value="-9";)
    [$epi_num]{
        [$esi_num]<float>(dsp="beta value", order="same as esi file")
        [$esi_num]<float>(dsp="se value", order="same as esi file")
    }(dsp="beta and se value of each probe"; order="same as epi file")

```

#### sparse file formate | SMR_SPARSE_3 SPARSE_BELT

```
    []<>(#besd sparse binary file)
    []<>(%deflable dsp "description of block")
    []<>(%deflable esi_index "index of esi snp/variant")
    []<>(endianness="little")
    [1]<int32>(dsp="besd type"; value="3 for SMR_SPARSE_3 SPARSE_BELT sparse format")  
    [1]<int32>(dsp="sample size", value="-9 for NA";)  
    [1]<int32; $esi_num>(dsp="esi number")  
    [1]<int32; $epi_num>(dsp="epi number")  
    [12]<int32>(value="-9")  
    [1]<uint64; $value_num; $value_num = 0; for(i = 1; i < $epi_num; i++){$value_num += @epi_num.$beta_offset + @epi_num.$se_offset}>(dsp="number of sparse beta and se value")  
    [1]<uint64>(value="0")
    [$epi_num; @]{  
        [1]<uint64; @epi_num.$beta_offset>(dsp="number of esi offset")
        [1]<uint64; @epi_num.$se_offset>(dsp="number of esi offset") 
    }(dsp="beta and se offsets number of each probe"; order="same as epi file")
    [$epi_num; @]{
        [@epi_num.$beta_offset; @]<uint32; $beta_index>(dsp="beta index of esi", order="esi file")
        [@epi_num.$se_offset; @]<uint32; $se_index>(dsp="se index of esi", order="esi file")
    }(dsp="beta and se esi index arrary of each probe", order="same as epi file")
    [$epi_num; @]{
        [@epi_num.$beta_offset]<float>(dsp="esi beta value"; esi_index=$beta_index)
        [@epi_num.$se_offset]<float>(dsp="esi se value"; esi_index=$se_index)
    }(dsp="beta as se value", order="epi file")

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
