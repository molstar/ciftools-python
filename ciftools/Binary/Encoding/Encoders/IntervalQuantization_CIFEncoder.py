import numpy as np

from ciftools.Binary.Encoding.Encoding import IntervalQuantizationEncoding, EEncoding
from ciftools.Binary.Encoding.data_types import DataTypes, EDataTypes
from ciftools.Binary.Encoding.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData


class IntervalQuantization_CIFEncoder(ICIFEncoder):
    def __init__(self, arg_min: int, arg_max: int, num_steps: int, array_type: EDataTypes = EDataTypes.Uint32):
        self._min = arg_min
        self._max = arg_max
        self._num_steps = num_steps
        self._array_type = array_type

    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        src_data_type: EDataTypes = DataTypes.from_dtype(data.dtype)

        if self._max < self._min:
            t = self._min
            self._min = self._max
            self._max = t

        encoding: IntervalQuantizationEncoding = {
            "min": self._min,
            "max": self._max,
            "numSteps": self._num_steps,
            "srcType": src_data_type,
            "kind": EEncoding.IntervalQuantization.name
        }

        dtype = DataTypes.to_dtype(self._array_type)

        if not len(data):
            return EncodedCIFData(data=np.empty(0, dtype=dtype), encoding=[encoding])

        delta = (self._max - self._min) / (self._num_steps - 1)

        quantized = np.clip(data, self._min, self._max)
        np.subtract(quantized, self._min, out=quantized)
        np.divide(quantized, delta, out=quantized)

        encoded_data = np.array(quantized, dtype=dtype)

        return EncodedCIFData(data=encoded_data, encoding=[encoding])
