# BOD file  

## .oii file
Columns are family ID, individual ID, paternal ID, maternal ID and sex (1=male; 2=female; 0=unknown). Missing data are represented by "NA".  

## .opi file 
Columns are chromosome, probe ID (can be the ID of an exon or a transcript for RNA-seq data), physical position, gene ID and gene orientation.  


## .bod file  
DNA methylation (or gene expression) data in binary format.

first 12 bytes:  
    [1]<char>(type of value. 0 for DNA methylation beta value, 1 for DNA methylation m value and 2 for any other type of value)
    [1]<char>(type of data. 0 for gene expression data, 1 for DNA methylation data, and 2 for any other type of data)
    [1]<char>(reserved)
    [1]<char>(reserved)
    [1|$1]<int32>(number of individual)
    [1|$2]<int32>(number of probe)
    [[$1] * [$2]]<double>(values, the length is equtal to number of individual * number of probe.)



