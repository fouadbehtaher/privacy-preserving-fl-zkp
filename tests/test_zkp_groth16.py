"""Groth16 training-integrity prototype: toy-size end-to-end tests with a LOCAL TEST setup.
Needs Node and `npm ci` in zkp-circuits/ (circom2, snarkjs, circomlib). Skipped if missing.
Not wired into the server: the API still rejects every update."""
import json, os, random, shutil, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import pytest
from client.zk_training import required_bits, train_int

CIRCUITS = os.path.join(ROOT, "zkp-circuits")
UTILS = os.path.join(ROOT, "zkp-utils")
T, N, F, K, M, BX = 2, 4, 3, 6, 8, 12

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None or not os.path.exists(os.path.join(CIRCUITS, "node_modules", ".bin", "snarkjs")),
    reason="node or zkp-circuits/node_modules missing (run npm ci in zkp-circuits)")


def node(*args, check=True):
    return subprocess.run(["node", *args], capture_output=True, text=True, check=check)


@pytest.fixture(scope="module")
def built():
    out = tempfile.mkdtemp()
    b1, b2 = required_bits(N, F, BX, K)
    node(os.path.join(UTILS, "setup_circuits.js"), out, *map(str, (T, N, F, K, M, BX, b1, b2)))
    yield out
    shutil.rmtree(out, ignore_errors=True)


def make_input(seed=1):
    rnd = random.Random(seed)
    x = [[rnd.randint(-40, 40) for _ in range(F)] for _ in range(N)]
    y = [rnd.randint(-40, 40) for _ in range(N)]
    w0 = [rnd.randint(-20, 20) for _ in range(F)]
    return {"w0": w0, "x": x, "y": y}


def prove(out, data, name="in.json"):
    path = os.path.join(out, name)
    json.dump(data, open(path, "w"))
    return node(os.path.join(UTILS, "generate_proof.js"), out, path, check=False)


def verify(out, pub=None, proof=None):
    pub = pub or os.path.join(out, "public.json")
    proof = proof or os.path.join(out, "proof.json")
    return node(os.path.join(UTILS, "verify_proof.js"), os.path.join(out, "vk.json"), pub, proof, check=False).returncode


def test_honest_proof_verifies_and_matches_reference(built):
    data = make_input()
    assert prove(built, data).returncode == 0
    assert verify(built) == 0
    pub = [int(v) for v in json.load(open(os.path.join(built, "public.json")))]
    expected = train_int(data["w0"], data["x"], data["y"], T, K, M)
    to_signed = lambda v: v if v < 2 ** 200 else v - 21888242871839275222246405745257275088548364400416034343698204186575808495617
    assert [to_signed(v) for v in pub[:F]] == expected  # public outputs: final weights
    assert pub[F:] == [v % 21888242871839275222246405745257275088548364400416034343698204186575808495617 for v in data["w0"]]


def test_changed_final_weights_are_rejected(built):
    assert prove(built, make_input(2)).returncode == 0
    pub = json.load(open(os.path.join(built, "public.json")))
    pub[0] = str(int(pub[0]) + 1)
    bad = os.path.join(built, "public_bad.json")
    json.dump(pub, open(bad, "w"))
    assert verify(built, pub=bad) != 0


def test_changed_initial_weights_are_rejected(built):
    assert prove(built, make_input(3)).returncode == 0
    pub = json.load(open(os.path.join(built, "public.json")))
    pub[F] = str(int(pub[F]) + 1)
    bad = os.path.join(built, "public_bad2.json")
    json.dump(pub, open(bad, "w"))
    assert verify(built, pub=bad) != 0


def test_proof_of_one_run_does_not_verify_another_runs_public_values(built):
    assert prove(built, make_input(4)).returncode == 0
    first_pub = open(os.path.join(built, "public.json")).read()
    first_proof = open(os.path.join(built, "proof.json")).read()
    assert prove(built, make_input(5)).returncode == 0
    a = os.path.join(built, "pub_a.json"); b = os.path.join(built, "proof_a.json")
    open(a, "w").write(first_pub); open(b, "w").write(first_proof)
    assert verify(built, pub=a, proof=b) == 0                      # its own pair is fine
    assert verify(built, pub=a) != 0                                # first public values + second proof


def test_out_of_range_data_gets_no_proof(built):
    data = make_input(6)
    data["x"][0][0] = 2 ** (BX - 1)  # just outside the allowed range
    assert prove(built, data).returncode != 0


def test_garbage_proof_is_rejected(built):
    assert prove(built, make_input(7)).returncode == 0
    junk = os.path.join(built, "junk.json")
    open(junk, "w").write("{}")
    assert verify(built, proof=junk) != 0
