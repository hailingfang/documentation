# GCTA BESD file

## .epi file

```
    [%file $epi_file]<>(file="epi file")
    [%let $epi_num = $filelen($epi_file)]<>()
    [$epi_num]{
        [1]<int>(dsp="chromosome")
        [1]<string>(dsp="probe id")
        [1]<float>(dsp="physical position")
        [1]<uint32>(dsp="base position")
        [1]<string>(dsp="oritation")
    }()
```

## .esi file

```
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
```

## .besd file

There kinds of file format of besd file. First is Dense file type, and second is sparse file type.

### Macros

Defined C macros for besd file format. 

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


### sparse and dense file formate | SMR_SPARSE_3 SPARSE_BELT & SMR_DENSE_3

```
    []<>(info="besd sparse and dense binary file")
    []<>(endianness="little")
    [%file $epi_file]<>(file="epi file")
    [%file $esi_file]<>(file="esi file")
    [%let $epi_flen = $filelen($epi_file)]<>()
    [%let $esi_flen = $filelen($esi_file)]<>()
    [1]<int32>(dsp="besd type"; value="3 for sparse, 5 for dense")
    [1]<int32>(dsp="sample number"; value="-9 if unknown")
    [1]<int32; $esi_num>(dsp="esi_num")
    [%assert $esi_num == $esi_flen]<>()
    [1]<int32; $epi_num>(dsp="epi_num")
    [%assert $epi_num == $epi_flen]<>()
    [12]<int32; = -9>(dsp="keeped for future")

    [%if $format == 5] {
        [$epi_num]{
            [$esi_num]<float>(dsp="beta value")
            [$esi_num]<float>(dsp="se value")
        }(dsp="beta and se value of each probe"; order="same as epi file")
    }()

    [%elif $format == 3] {
        [%let $value_num = 0]<>()
        [1]<uint64; = $:value_num>(dsp="value number")
        [1]<uint64; = 0; @beta_se_offset; $se_offset>(dsp="first value of offset")
        [$epi_num]{
            [1]<uint64; +@beta_se_offset; +$value_num>(dsp="beta offset")
            [1]<uint64; +@beta_se_offset; +$value_num>(dsp="se offset")
        }
        [$epi_num; ~i] {
            [@beta_offset[2 * $i + 1] - @beta_offset[2 * $i]]<uint32>(dsp="index of beta")
            [@beta_se_offset[2 * $i + 2] - @beta_se_offset[2 * $i + 1]]<uint32>(dsp="index of se")
        }
        [$epi_num; ~i] {
            [@beta_offset[2 * $i + 1] - @beta_offset[2 * $i]]<float>(dsp="index of beta")
            [@beta_se_offset[2 * $i + 2] - @beta_se_offset[2 * $i + 1]]<float>(dsp="index of se")   
        }
    }()

    [%else]{
        [%error]<>(mesg="format not recognized")
    }()

```

## SMR_SPARSE_3F 0x40400000

```
    # !Need correct

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

```
