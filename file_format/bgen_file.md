# BGEN file format


## version 1.2

```
[1]<uint32>(name="offset"; description="relative to the fifth byte of the file, of the first byte of the first variant data block")
[1]<uint32; $len_head>(name="head length in byte";)
[1]<uint32; $M>(name="variant block number")
[1]<uint32; $N>(name="sample number")
[$len_head - 20]<byte>(name="free data")
{
    [2]<bit>(name="compress snp block"; value_choice="0: not compressed, 1: compressed")
    [4]<bit>(name="layout"; value_choice="0: layout 0. 1: layout 1, version 1.1. 2: layout 2, version 1.2.")
    [25]<bit>()
    [1]<bit; $sample_flag>(name="sampleIdentifier"; value_choice="0: sample identifier is not stored. 1: sample are stored")

}(name="flags")
[1 if $sample_falg == 1 else 0]{}(name="sample identifier block")
```