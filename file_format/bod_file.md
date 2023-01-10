# BOD file  

## .oii file
Columns are:

`"family ID" "individual ID" "paternal ID" "maternal ID" "sex"`.

 `sex`: 1 for male; 2 for female; 0 for unknown.

Missing data are represented by "NA".  

## .opi file 
Columns are:

`"chromosome" "probe ID" "physical position" "gene ID" "gene orientation"`.  

`probe ID`: can be the ID of an exon or a transcript for RNA-seq data)

## .bod file  
Binary file of DNA methylation (or gene expression) data.
```
[]<>(#bod binary data.)
[]<>(%deflable dsp "description of elemental block")
[]<>(endianness="little")
[1]<char>(dsp="value type"; value="0 for DNA methylation beta value, 1 for DNA methylation m value and 2 for any other type of value")
[1]<char>(dsp="data type"; value="0 for gene expression data, 1 for DNA methylation data, and 2 for any other type of data")
[2]<char>(dsp="reserved"; value="0")
[1]<uint32; $indi_num>(dsp="number of individual")
[1]<uint32; $probe_num>(dsp="number of probe")
[$probe_num]{
    [$indi_num]<double>(dsp="data of each"; order="same as oii file")
}(dsp="data for each probe"; order="same as opi file")

```


