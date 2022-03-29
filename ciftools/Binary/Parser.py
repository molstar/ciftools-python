from typing import Union

import msgpack
import numpy as np

from ciftools.CIFFormat.Implementations.BinaryCIF.binary_cif_file import BinaryCIFFile
from ciftools.CIFFormat.i_cif_file import ICIFFile


class BinaryCifParser:

    @staticmethod
    def __checkVersions(min_ver: list[int], current_ver: list[int]):
        for i in range(2):
            if min_ver[i] > current_ver[i]:
                return False

        return True

    @staticmethod
    def parse(data: Union[np.ndarray, bytes, list]) -> ICIFFile:
        min_version = [0, 3];

        try:
            array = bytes(data)

            unpacked = msgpack.loads(array)
            #if not __checkVersions(min_version, unpacked.version.match(/(\d)\.(\d)\.\d/).slice(1))) {
            #    return ParserResult.error<CIFTools.File>(`Unsupported format version. Current ${unpacked.version}, required ${minVersion.join('.')}.`);
            #}
            print("DEBUG_PARSED: " + str(unpacked))  # TODO: unpacked is supposed to be of type Encoded CIF Data
            file = BinaryCIFFile(unpacked)
            return file

        except Exception:
            raise
