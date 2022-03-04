from src.Binary.Encoding import DataTypes

_dtypes = {
    DataTypes.Int8: "i1",
    DataTypes.Int16: "i2",
    DataTypes.Int32: "i4",
    DataTypes.Uint8: "u1",
    DataTypes.Uint16: "u2",
    DataTypes.Uint32: "u4",
    DataTypes.Float32: "f4",
    DataTypes.Float64: "f8",
}


def get_dtype(data_type: DataTypes) -> str:
    if data_type in _dtypes:
        return _dtypes[data_type]

    raise ValueError(f"Unsupported data type '{data_type}'")