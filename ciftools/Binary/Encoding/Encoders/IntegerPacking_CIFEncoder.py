import math

import numpy as np
from ciftools.Binary.Encoding.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from ciftools.Binary.Encoding.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding import EEncoding, IntegerPackingEncoding
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData
from numpy import int8, int16, uint8, uint16


class IntegerPacking_CIFEncoder(ICIFEncoder):
    class __packing__:
        isSigned: bool
        size: int
        bytesPerElement: int

    def __init__(self):
        self.byte_array_encoder = ByteArray_CIFEncoder()

    def encode(self, data: np.ndarray) -> EncodedCIFData:

        # TODO: must be 32bit integer

        packing = IntegerPacking_CIFEncoder.__determine_packing__(data)
        if packing.bytesPerElement == 4:
            return self.byte_array_encoder.encode(data)

        # integer packing

        if packing.isSigned:
            if packing.bytesPerElement == 1:
                upper_limit = 0x7F
                packed = np.empty(packing.size, dtype=int8)
            else:
                upper_limit = 0x7FFF
                packed = np.empty(packing.size, dtype=int16)
        else:
            if packing.bytesPerElement == 1:
                upper_limit = 0xFF
                packed = np.empty(packing.size, dtype=uint8)
            else:
                upper_limit = 0xFFFF
                packed = np.empty(packing.size, dtype=uint16)

        lower_limit = -upper_limit - 1
        data_len = len(data)

        packed_index = 0
        for i in range(data_len):
            value = data[i]
            if value >= 0:
                while value >= upper_limit:
                    packed[packed_index] = upper_limit
                    packed_index += 1
                    value -= upper_limit
            else:
                while value <= lower_limit:
                    packed[packed_index] = lower_limit
                    packed_index += 1
                    value -= lower_limit

            packed[packed_index] = value
            packed_index += 1

        byte_array_result = self.byte_array_encoder.encode(packed)

        integer_packing_encoding: IntegerPackingEncoding = {
            "kind": EEncoding.IntegerPacking.name,
            "isUnsigned": not packing.isSigned,
            "srcSize": data_len,
            "byteCount": packing.bytesPerElement
        }

        return EncodedCIFData(
            data=byte_array_result['data'],
            encoding=[integer_packing_encoding, byte_array_result["encoding"][0]])

    @staticmethod
    def __packing_size__(data: np.ndarray, upper_limit: int) -> int:
        lower_limit = -upper_limit - 1
        size = 0

        data_len = len(data)
        for i in range(data_len):
            value = data[i]
            if value == 0:
                size = size + 1
            elif value > 0:
                size = size + math.ceil(value/upper_limit)
                if value % upper_limit == 0:
                    size = size + 1
            else:
                size = size + math.ceil(value/lower_limit)
                if value % lower_limit == 0:
                    size = size + 1

        return size

    @staticmethod
    def __determine_packing__(data: np.ndarray) -> __packing__:

        data_len = len(data)

        # determine sign
        is_signed = False
        for i in range(len(data)):
            if data[i] < 0:
                is_signed = True
                break

        # determine packing size
        size8 = (
            IntegerPacking_CIFEncoder.__packing_size__(data, 0x7F)
            if is_signed
            else IntegerPacking_CIFEncoder.__packing_size__(data, 0xFF)
        )
        size16 = (
            IntegerPacking_CIFEncoder.__packing_size__(data, 0x7FFF)
            if is_signed
            else IntegerPacking_CIFEncoder.__packing_size__(data, 0xFFFF)
        )

        packing = IntegerPacking_CIFEncoder.__packing__()
        packing.isSigned = is_signed

        if data_len * 4 < size16 * 2:
            packing.size = data_len
            packing.bytesPerElement = 4

        elif size16 * 2 < size8:
            packing.size = size16
            packing.bytesPerElement = 2

        else:
            packing.size = size8
            packing.bytesPerElement = 1

        return packing
