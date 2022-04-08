const msgpack = require('molstar/lib/commonjs/mol-io/common/msgpack/decode');
const cif = require('molstar/lib/commonjs/mol-io/reader/cif');
const fs = require('fs');
const data = fs.readFileSync('../ciftools/tests/lattices.bcif');
const decoded = msgpack.decodeMsgPack(new Uint8Array(data));
// console.log(decoded.dataBlocks[1].categories[0].columns.slice(-1)[0].data.encoding);

async function test() {
    const { result } = await cif.CIF.parseBinary(new Uint8Array(data)).run();
    const annotation = result.blocks[1].categories.volume.getField('annotation');
    console.log(annotation.binaryEncoding[0].dataEncoding);
    console.log(annotation);
}

test()