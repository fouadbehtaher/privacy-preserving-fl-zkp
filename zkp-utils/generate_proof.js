// Create a Groth16 proof of training integrity.
// usage: node zkp-utils/generate_proof.js OUTDIR INPUT.json
// INPUT.json: {"w0":[...], "x":[[...]], "y":[...]} integers (value * 2^K). x and y stay private.
// Writes OUTDIR/proof.json and OUTDIR/public.json (public = wT outputs then w0).
// Fails (no proof) if the data breaks a range bound or the circuit constraints.
const { execFileSync } = require('child_process');
const path = require('path');
const [out, input] = process.argv.slice(2);
if (!input) { console.error('usage: generate_proof.js OUTDIR INPUT.json'); process.exit(2); }
const root = path.resolve(__dirname, '..', 'zkp-circuits');
const snark = path.join(root, 'node_modules', '.bin', 'snarkjs');
const wasm = path.join(out, 'main_js', 'main.wasm');
const wit = path.join(out, 'witness.wtns');
execFileSync('node', [path.join(out, 'main_js', 'generate_witness.js'), wasm, input, wit], { stdio: 'pipe' });
execFileSync(snark, ['groth16', 'prove', path.join(out, 'circuit.zkey'), wit, path.join(out, 'proof.json'), path.join(out, 'public.json')], { stdio: 'pipe' });
require('fs').unlinkSync(wit);
console.log('proof written:', path.join(out, 'proof.json'));
