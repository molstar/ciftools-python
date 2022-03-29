import numpy as np
from ciftools.Binary.data_types import DataTypes, EDataTypes
from ciftools.Binary.Encoding.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding import EEncoding, IntervalQuantizationEncoding
from ciftools.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData


class IntervalQuantization_CIFEncoder(ICIFEncoder):
    def __init__(self, arg_min: int, arg_max: int, num_steps: int):
        self._min = arg_min
        self._max = arg_max
        self._num_steps = num_steps

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

        if not len(data):
            return EncodedCIFData(data=np.empty(0), encoding=[encoding])

        delta = (self._max - self._min) / (self._num_steps - 1)
        print(delta)
        encoded_data = np.zeros(len(data))
        for i in range(len(data)):
            data_point = data[i]
            if data_point >= self._max:
                encoded_data[i] = self._num_steps
            elif data_point > self._min:
                encoded_data[i] = round((data_point - self._min) / delta)
            else:
                encoded_data[i] = 0

        return EncodedCIFData(data=encoded_data, encoding=[encoding])
