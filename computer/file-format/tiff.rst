.. code::

    [# TIFF v6.0]
    {
        [2]<char; ={['I', 'I'], ['M', 'M']}>(dsp="byte order")
        [1]<uint16; =42>(dsp="the value is 42 if interperated the int in correct order")
        [1]<uint32;len_to_first_IFD>(dsp="The offset (in bytes) of the first IFD.")
    }(dsp="IFH")

    
    [len_to_first_IFD - 8]<byte>
    
    {
        [1]<uint16>(dsp="IFD entry number")
        {
            [2]<byte>()
            [2]<byte>()
            [1]<uint32>()
            [1]<uint32>()
        }

    }(dsp="IFD")

