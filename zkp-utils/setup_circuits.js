// Build the training-integrity circuit for one parameter set and run a LOCAL Groth16 setup.
// usage: node zkp-utils/setup_circuits.js OUTDIR T N F K M BX B1 B2 [PTAU_POWER]  (power defaults to the smallest that fits)
// WARNING: the powers-of-tau and zkey contributions here come from one machine, so this is
// a TEST setup only. Keys made this way must never be trusted for real use.
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const [out, T, N, F, K, M, BX, B1, B2, POW_ARG] = process.argv.slice(2);
if (!B2) { console.error('usage: setup_circuits.js OUTDIR T N F K M BX B1 B2 [PTAU_POWER]'); process.exit(2); }
const root = path.resolve(__dirname, '..', 'zkp-circuits');
const bin = (n) => path.join(root, 'node_modules', '.bin', n);
const run = (cmd, args) => execFileSync(cmd, args, { stdio: ['ignore', 'pipe', 'pipe'] }).toString();
const entropy = () => crypto.randomBytes(16).toString('hex');

fs.mkdirSync(out, { recursive: true });
const main = path.join(out, 'main.circom');
fs.copyFileSync(path.join(root, 'training_integrity.circom'), path.join(out, 'training_integrity.circom'));
fs.writeFileSync(main,
  `pragma circom 2.0.0;\ninclude "training_integrity.circom";\n` +
  `component main {public [w0]} = TrainingIntegrity(${T},${N},${F},${K},${M},${BX},${B1},${B2});\n`);
fs.writeFileSync(path.join(out, 'params.json'), JSON.stringify({ T: +T, N: +N, F: +F, K: +K, M: +M, BX: +BX, B1: +B1, B2: +B2 }));

// circom2 (the wasm build of circom) resolves relative paths only, so copy circomlib next to the
// circuit and run it from the build dir.
fs.cpSync(path.join(root, 'node_modules', 'circomlib'), path.join(out, 'circomlib'), { recursive: true });
execFileSync(bin('circom2'), ['main.circom', '--r1cs', '--wasm', '-l', '.', '-o', '.'],
  { cwd: path.resolve(out), stdio: ['ignore', 'pipe', 'pipe'] });
const r1cs = path.join(out, 'main.r1cs');
const info = run(bin('snarkjs'), ['r1cs', 'info', r1cs]);
console.log(info.replace(/\x1b\[[0-9;]*m/g, '').split('\n').filter((l) => /Constraints|Inputs|Outputs/.test(l)).join('\n'));

const nCons = Number((info.replace(/\x1b\[[0-9;]*m/g, '').match(/Constraints:\s*(\d+)/) || [])[1]);
const clean = info.replace(/\x1b\[[0-9;]*m/g, '');
const nIO = Number((clean.match(/Public Inputs:\s*(\d+)/) || [])[1]) + Number((clean.match(/Outputs:\s*(\d+)/) || [])[1]);
// groth16 setup needs 2^power >= constraints + public wires + 1
const POW = POW_ARG || String(Math.max(8, Math.ceil(Math.log2(nCons + nIO + 1))));
const p0 = path.join(out, 'p0.ptau'), p1 = path.join(out, 'p1.ptau'), pf = path.join(out, 'pf.ptau');
run(bin('snarkjs'), ['powersoftau', 'new', 'bn128', POW, p0]);
run(bin('snarkjs'), ['powersoftau', 'contribute', p0, p1, '--name=local-test', `-e=${entropy()}`]);
run(bin('snarkjs'), ['powersoftau', 'prepare', 'phase2', p1, pf]);
const z0 = path.join(out, 'z0.zkey'), z1 = path.join(out, 'circuit.zkey');
run(bin('snarkjs'), ['groth16', 'setup', r1cs, pf, z0]);
run(bin('snarkjs'), ['zkey', 'contribute', z0, z1, '--name=local-test', `-e=${entropy()}`]);
run(bin('snarkjs'), ['zkey', 'export', 'verificationkey', z1, path.join(out, 'vk.json')]);
for (const f of [p0, p1, z0]) fs.unlinkSync(f);
console.log('setup done (TEST setup, not trusted):', out);
