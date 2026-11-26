// Verify a Groth16 training-integrity proof.
// usage: node zkp-utils/verify_proof.js VK.json PUBLIC.json PROOF.json
// Exit code 0 only if the proof verifies; anything else (including errors) is a rejection.
const { execFileSync } = require('child_process');
const path = require('path');
const [vk, pub, proof] = process.argv.slice(2);
if (!proof) { console.error('usage: verify_proof.js VK.json PUBLIC.json PROOF.json'); process.exit(2); }
const snark = path.join(path.resolve(__dirname, '..', 'zkp-circuits'), 'node_modules', '.bin', 'snarkjs');
try {
  const o = execFileSync(snark, ['groth16', 'verify', vk, pub, proof], { stdio: 'pipe' }).toString();
  if (/OK!/.test(o)) { console.log('VALID'); process.exit(0); }
  console.log('INVALID'); process.exit(1);
} catch (e) { console.log('INVALID'); process.exit(1); }
