# BED file

## .fam file
A text file without header line. and one line per sample with six fields.
1. Family ID
2. Within-family ID(cannot be '0')
3. Within-family ID of father('0' if father isn't in dataset)
4. Within-family ID of mother('0' if mother isn't in dataset)
5. sex code('1' for male, '2' for female, '0' for unknown)
6. Phenotype value('1' for control, '2' for case, '-9'/'0' for missing data)


## .bim file  
extended variant information file accompanying a .bed binary genotype table. have no
header line, and each line contain six fields.
1. chromosome code(and integer or X, Y, XY, MT, 0 indicate unknown)
2. variant identifier
3. position in morgans or centimorgans
4. base pair coordinate
5. allele 1
6. allele 2

## .bed file

    [3]<char>(magic number, in lasted plink version, them should be 0x6c, 0x1b, 0x01)  
    {
        [N / 4]<char>(N is number of sample of .fam. if N is not divisible by 4, the extra high order bits in last byte of each block are always zero.)  
        [N / 4]<char>()()  
        ...
    }:(here are V time replication, each represent a variant of .bim)


every of 2 bits of a byte for genotype.  
* 00: Homozygous of first allele in .bim file.
* 10: Heterozygous.
* 11: Homozygous of second allele in .bim file.
* 01: Missing

## reference
[bed file](https://www.cog-genomics.org/plink/1.9/formats)
[plink2R](https://github.com/gabraham/plink2R/blob/master/plink2R/src/data.cpp)
