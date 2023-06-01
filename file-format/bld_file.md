# bld file formte

    [1]<int>(0 or 1, 0 for ld r, 1 for ld r^2)
    [1]<int>(bdata.keep)
    [1|$1]<int>(snp_num?)
    [1]<int>(ldwind)
    [12](int)(-9)
    [1|$2]<uint64>(number of value)
    [1]<uint64>(0)
    [$1]<uint64>(value's offset of each snp)
    [$2]<float>(values)