GCTA BESD file
===================

The BESD file is a binary file format used in GCTA, OSCA, and SMR to store 
GWAS analysis results. It must be accompanied by the .epi and .esi files when used.


Epi file
-------------------

The Epi file is a plaintext file where every line represents an entry of
information for a phenotype. Therefore, the number of lines in the .epi file is
equal to the number of phenotypes.

FLML description
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    def filetype plaintext;
    def encode ascii;
    export line_num;
    export line_order;

    [+:line_num]{
        [1]<string>(name="chromosome number")
        [1]<string>(name="variant ID")
        [1]<string>(name="physical position"; datatype=float)
        [1]<string>(name="base position"; datatype=int)
        [1]<string>(name="orientation"; choices={"+", "-"})
    }(element_end="\n"; element_sub_sep_file_scope={"\s", "\t"}; order=line_order)


Esi file
-----------------

The Esi file is used to record information of variants.

FLML description
~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    def filetype plaintext;
    def encode ascii;
    export line_num;
    export line_order;
    export file_data;

    file_data = [];
    [+:line_num]{
        [1]<string; :chrom>(name="chromosome")
        [1]<string; :rsid>(name="rsid")
        [1]<string; :pos>(name="physical position"; datatype=float)
        [1]<string; :base_pos>(name="base position"; datatype=uint)
        [1]<string; :a1>(name="reference allel")
        [1]<string; :a2>(name="alternertive allel")
        [1]<string; :freq>(name="minor allel frequency"; datatype=float)
        file_data.append([chrom, rsid, pos, base_pos, a1, a2, freq]);
    }(element_end="\n"; element_sub_sep_file_scope=("\s", "\t"); order=line_order)



Besd file
-----------------------

There kinds of file format of besd file. First is Dense file type, and second is sparse file type.

Macros
~~~~~~~~~~~~~~~~~~~

Defined C macros for besd file format. 

* Dense

::

    #define DENSE_FULL 0
    #define DENSE_BELT 1
    #define OSCA_DENSE_1 4 // 0x00000004: RESERVEDUNITS*ints  + floats  :  <beta, se> for each SNP across all the probes are adjacent.
    #define SMR_DENSE_1 0 // 0x00000000 + floats  : beta values (followed by se values) for each probe across all the snps are adjacent.
    #define SMR_DENSE_3 5  // RESERVEDUNITS*ints + floats (indicator+samplesize+snpnumber+probenumber+ 12*-9s + values) [SMR default and OSCA default]

* Sparse

::

    #define SPARSE_FULL 2
    #define SPARSE_BELT 3
    #define OSCA_SPARSE_1 1 // 0x00000001: RESERVEDUNITS*ints + uint64_t  + uint64_ts + uint32_ts + floats: value number + (half uint64_ts and half uint32_ts of SMR_SPARSE_3) [OSCA default]
    #define SMR_SPARSE_3F 0x40400000 // 0x40400000: uint32_t + uint64_t + uint64_ts + uint32_ts + floats
    #define SMR_SPARSE_3 3 // RESERVEDUNITS*ints + uint64_t + uint64_ts + uint32_ts + floats (indicator+samplesize+snpnumber+probenumber+ 6*-9s +valnumber+cols+rowids+betases) [SMR default]


Sparse and Dense file formate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    def filetype binary;
    def endianness little;
    import epi_format;
    import esi_format;
    reqire epi_file;
    reqire esi_file;

    [1]<int32; :file_format>(name="format marker"; choices={3, 5})
    [1]<uint32>(name="sample number"; NA=-9)
    [1]<uint32; :esi_len>(name="number of variants")
    assert esi_len == esi_format.line_num;
    [1]<uint32; :epi_len>(name="number of probes")
    assert epi_len == epi_format.line_num;
    [12]<int32; []=-9>(name="coserved bytes")

    if (file_format == 5){
        [epi_num] {
            [esi_num]<float>(name="beta values of one probe"; align_with=esi_format.line_order)
            [esi_num]<float>(name="se values of one probe"; align_with=esi_format.line_order)
        }(name="probe data"; align_with=epi_format.line_order)
    }

    if (file_format == 3){

        [1]<uint64; :value_num>(name="the number of values"; dsp="inlcude beta and se values")
        [1]<uint64; =0>(name="first offset")
        
        beta_value_s = [];
        se_value_s = [];
        last_offset = 0;
        [epi_len]{
            [1]<uint64; :beta_offset>(name="totall offset of beta data")
            [1]<uint64; :se_offset>(name="totall offset of se data")
            beta_num = beta_offset - last_offset;
            last_offset = beta_offset;
            se_num = se_offset - last_offset;
            last_offset = se_offset;
            assert beta_num == se_num;
            beta_value_s.append(beta_num);
            se_value_s.append(se_num);
        }(name="data offset of probes"; align_with=epi_format.line_order)

        orders = [];
        for (i = 0; i < epi_len; i++) {
            [beta_value_s[i]]<uint32; beta_idx>(name="index for esi of beta"; correspond=esi_format.file_data[beta_idx]; order=beta_order)
            [se_value_s[i]]<uint32; :se_idx>(name="index for esi of se"; align_with=esi_format.file_data[se_idx])
            orders.append(beta_order);
        }
    
        for (i = 0; i < epi_len; i++) {
            [beta_value_s[i]]<float>(name="beta values"; align_with=orders[i])
            [se_value_s[i]]<float>(name="se values"; align_with=orders[i])
        }
    }

