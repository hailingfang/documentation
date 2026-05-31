TIFF file format
==============================

The TIFF v6.0 format described by FLML.

.. code::

    [# TIFF v6.0]
    #Image File Header
    [2]<char>(name="byte order"; id="byte_oder"; choices={['I','I'], ['M','M']})
    [1]<uint16; =42>(name="magic number")
    [1]<uint32; :offset_to_first_IFD>(id="offset_to_first_IFD")

    if (offset_to_first_IFD >= 8) {
        tag_info = {}
        goto (offset_to_first_IFD) {
            [1]<uint16; :entry_num>(name="entry number")
            [entry_num]{
                [1]<uint16; :tag_id>
                [1]<uint16; :tag_data_type>
                [1]<uint32; :tag_data_type_count>
                [4]<byte; :value_or_offset>
                key, value = get_tag_info(tag_id, tag_data_type, tag_data_type_count, value_or_offset);
                tag_info[key] = value;
            }
            [1]<uint32; offset_to_next_IFD>        
        }
        i = 0;
        for (stripoffset in tag_info["StripOffsets"]) {
            goto (stripoffset) {
                [tag_info["StripByteCounts"][i] / (sum(tag_info["BitsPerSample"]) / 8) / tag_info["ImageWidth"]]{
                    [tag_info[ImageWidth]]{
                        [sum(tag_info["BitsPerSample"]) / 8]<byte>
                    }
                }
                [tag_info["StripByteCounts"][i]] {
                    [3]<byte>
                }
            }
            i += 1;
        }
    }


    fun get_tag_data_type(data_type) {
        if (data_type == 1) {
            data_type = [1, 1, "uint8"];
        } elif (data_type == 2) {
            data_type = [1, 1, "char"];
        } elif (data_type == 3) {
            data_type = [2, 2, "uint16"];
        } elif (data_type == 4) {
            data_type = [4, 4, "uint32"];
        } elif (data_type == 5) {
            data_type = [8, 4, "uint32"];
        } elif (data_type == 6) {
            data_type = [1, 1, "int8"];
        } elif (data_type == 7) {
            data_type = [1, 1, "byte"];
        } elif (data_type == 8) {
            data_type = [2, 2, "int16"]; 
        } elif (data_type == 9) {
            data_type = [4, 4, "int32"];
        } elif (data_type == 10) {
            data_type = [8, 4, "int32"];
        } elif (data_type == 11) {
            data_type = [4, 4, "float"];
        } elif (data_type == 12) {
            data_type == [8, 8, "double"];
        } else {
            raise Exception("unkown data type");
        } 
        return data_type;    
    }


    fun byte_to_int(bytes_arr, int_type, int_bytes_len, int_num) {
        int_s = [];
        if (int_type == "uint") {
            for (i = 0; i < int_num; i++) {
                n = 0;
                for (j = 0; j < int_bytes_len; j++) {
                    n += byte_arr[i * int_bytes_len + j] * 255**j;
                }
            }
        }
        return int_s;
    }

    fun get_tag_info(tag_id, tag_data_type, tag_data_type_count, value_or_offset) {
        if (tag_id == 256) {
            tag_data_type = get_tag_data_type(tag_data_type); #[2, 2, "uint16"]
            return "ImageWidth", byte_to_int(value_or_offset, "uint", tag_data_type[1], 1)[0]
        }
        elif (tag_id == 257) {
            tag_data_type = get_tag_data_type(tag_data_type);
            return "ImageLength", byte_to_int(value_or_offset, "uint", tag_data_type[1], 1)[0];
        }
        elif (tag_id == 258) {
            tag_data_type = get_tag_data_type(tag_data_type);
            if (tag_data_type[0] * tag_data_type_count > 4) {
                seek_pos = byte_to_int(value_or_offset, "uint", tag_data_type[1], 1)[0];
                fileself.seek(seek_pos);
                return "BitsPerSample", fileself.read(tag_data_type[1] * tag_data_type_count);
            }
            else {
                return "BitsPerSample", byte_to_int(value_or_offset, "uint", tag_data_type[1], tag_data_type_count);
            }
        }
        elif (tag_id == 259) {
            return "Compression", byte_to_int(value_or_offset, "uint", 2, 1)[0];
        }
        elif (tag_id == 262) {
            return "PhotometricInterpretation", byte_to_int(value_or_offset, "uint", 2, 1)[0];
        }
        elif (tag_id == 273) {
            tag_data_type = get_tag_data_type(tag_data_type);
            if (tag_data_type[0] * tag_data_type_count > 4) {
                seek_pos = byte_to_int(value_or_offset, "uint" tag_data_type[1], 1)[0];
                fileself.seek(seek_pos);
                bytes_arr = fileself.read(tag_data_type[1] * tag_data_type_count);
                return "StripOffsets", byte_to_int(bytes_arr, "uint", tag_data_type[1], tag_data_type_count);
            }
            else {
                return "StripOffsets", byte_to_int("uint", value_or_offset, 2, tag_data_type_count);
            }
        }
        elif (tag_id == 274) {
            return "SamplesPerPixel", byte_to_int(value_or_offset, "uint", 2, 1)[0];
        }
        elif (tag_id == 278) {
            return "RowsPerStrip", byte_to_int(value_or_offset, "uint", 2, 1)[0];
        }
        elif (tag_id == 279) {
            tag_data_type = get_tag_data_type(tag_data_type);
            if (tag_data_type[0] * tag_data_type_count > 4) {
                seek_pos = byte_to_int("uint", value_or_offset, tag_data_type[1], 1)[0];
                fileself.seek(seek_pos);
                byte_arr = fileself.read(tag_data_type[1] * tag_data_type_count);
                return "StripOffsets", byte_to_int(byte_arr, "uint", tag_data_type[1], tag_data_type_count);
            }
            else {
                return "StripOffsets", byte_to_int(value_or_offset, "uint", 2, tag_data_type_count);
            }                    
        }    
    }

    [#Notes
        byte_oder:
            Two char to indicate byte order, can be "II" for little ednian
            or "MM" for big endian.

        offset_to_first_IFD:
            The offset to the first IFD(Image File Directory).

    ]

    [#Reference
    1. https://www.fileformat.info/format/tiff/egff.htm   
    
    ]