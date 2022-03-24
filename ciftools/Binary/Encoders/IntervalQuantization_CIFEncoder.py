import numpy as np

from ciftools.Binary.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding import ByteArrayEncoding, IntervalQuantizationEncoding, EEncoding
from ciftools.Binary.data_types import DataTypes, EDataTypes
from ciftools.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData


class IntervalQuantization_CIFEncoder(ICIFEncoder):
    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        arg_min: int = kwargs["min"]
        arg_max: int = kwargs["max"]
        arg_num_steps = kwargs["num_steps"]
        src_data_type: EDataTypes = DataTypes.from_dtype(data.dtype)

        if arg_max < arg_min:
            t = arg_min
            arg_min = arg_max
            arg_max = t

        encoding = IntervalQuantizationEncoding()
        encoding["min"] = arg_min
        encoding["max"] = arg_max
        encoding["numSteps"] = arg_num_steps
        encoding["srcType"] = src_data_type
        encoding["kind"] = EEncoding.IntervalQuantization.name

        if not len(data):
            return EncodedCIFData(data=np.empty(0), encoding=[encoding])

        delta = (arg_max - arg_min) / (arg_num_steps - 1)
        print(delta)
        encoded_data = np.zeros(len(data))
        for i in range (len(data)):
            data_point = data[i]
            if data_point >= arg_max:
                encoded_data[i] = arg_num_steps
            elif data_point > arg_min:
                encoded_data[i] = round((data_point-arg_min)/delta)
            else:
                encoded_data[i] = 0

        return EncodedCIFData(data=encoded_data, encoding=[encoding])
