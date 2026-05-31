TIFF file format
==============================

The TIFF v6.0 format described by FLML.

.. code::

    [# TIFF v6.0]
    //Image File Header
    [2]<char>(name="byte order"; id="byte_oder"; choices={['I','I'], ['M','M']})
    [1]<uint16; =42>
    [1]<uint32; :offset_to_first_IFD>(id="offset_to_first_IFD")

    [if (offset_to_first_IFD >= 8)] {
        [tags = []]
        [goto offset_to_first_IFD] {
            [1]<uint16; tag_num>(name="entry number")
            [tag_num]{
                [1]<uint16; :tag_id>(name="tag id")
                [1]<uint16; :data_type>(name"data type"; greateqthan=1; lesseqthan=12)
                [1]<uint32; :data_count>(name="data count")
                [4]<byte; :data_value_offset>(name="data value or offset")
                tags.append([tag_id, data_type, data_count, data_value_offset])
            }(name="tag")

            width, height = get_image_width_height(tags)

            [1]<uint32; offset_to_next_IFD>        
        }

    } [else] {
        [print("empty TIFF file")]
    }

    [fun get_image_width_height(tags)] {
        width = 0;
        height = 0;
        for (tag in tags) {
            tag_id, data_type, data_count, data_value_offset = tag;
            if (tag_id == 256) {
                assert data_count == 1;
                assert get_tag_data_type(data_type)[0] <= 4;
                width = byte_to_int(data_value_offset, "uint32", 1)[0];
            }
            if (tag_id == 257) {
                assert data_count == 1;
                assert get_tag_data_type(data_type)[0] <= 4;
                height = byte_to_int(data_value_offset, "uint32", 1)[0];
            }
        }
        return width, height;
    }

    [fun get_image_data_offset(tags)] {
        offset = 8;
        for (tag in tags) {
            tag_id, data_type, data_count, data_value_offset = tag;
            if (tag_id == 273) {
                assert data_count == 1;
                assert get_tag_data_type(data_type)[0] <= 4;
                return byte_to_int(data_value_offset, "uint32", 1)[0];
            }
        }
    }

    [fun get_bitpersample(tags)] {
        bitpersample = [8, 8, 8];
        for (tag in tags) {
            tag_id, data_type, data_count, data_value_offset = tag;
            if (tag_id == 258) {
                data_type = get_tag_data_type(data_type);
                if (data_type[0] * data_count > 4) {
                    fileself.open("rb");
                    fileself.seek(byte_to_int(data_value_offset, "uint32", 1)[0], 0);
                    bitpersample = file.read(data_type[1], data_count);
                    fileself.close();
                    return bitpersample;
                }
                return byte_to_int(data_value_offset, data_type[1], data_count);
            }
        }

    }

    [fun get_compression_status(tag)] {
        for (tag in tags) {
            if (tag == 259) {
                data_value_offset = byte_to_int(data_value_offset, "uint16", 1)[0];
                if (data_value_offset == 1) {
                    return "uncompressed";
                }

                if (data_value_offset == 2) {
                    return "ccit";
                }
                //here some compression statue not judged
            }
        }
        return None;
    }



    [fun get_tag_data_type(data_type)] {
        if (data_type == 1) {
            data_type = [1, "uint8"];
        } elif (data_type == 2) {
            data_type = [1, "char"];
        } elif (data_type == 3) {
            data_type = [2, "uint16"];
        } elif (data_type == 4) {
            data_type = [4, "uint32"];
        } elif (data_type == 5) {
            data_type = [8, "uint32"];
        } elif (data_type == 6) {
            data_type = [1, "int8"];
        } elif (data_type == 7) {
            data_type = [1, "byte"];
        } elif (data_type == 8) {
            data_type = [2, "int16"]; 
        } elif (data_type == 9) {
            data_type = [4, "int32"];
        } elif (data_type == 10) {
            data_type = [8, "int32"];
        } elif (data_type == 11) {
            data_type = [4, "float"];
        } elif (data_type == 12) {
            data_type == [8, "double"];
        } else {
            print("error");
            raise Exception;
        } 
        return data_type;    
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