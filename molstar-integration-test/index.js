const msgpack = require('molstar/lib/commonjs/mol-io/common/msgpack/decode');
const fs = require('fs');
const data = fs.readFileSync('../ciftools/tests/lattices.bcif');
const decoded = msgpack.decodeMsgPack(new Uint8Array(data));
console.log(decoded.dataBlocks[1].categories[0].columns[1].data.encoding);