import base64, json, subprocess, sys
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
ROOT=Path(__file__).resolve().parents[1]
TOOL=ROOT/'scripts'/'contract_verifier.py'

def run(*args):
    return subprocess.run([sys.executable, str(TOOL), *map(str,args)], cwd=ROOT, text=True, capture_output=True, timeout=10)

def manifest():
    return {"schema_version":1,"run_id":"test-run-01","package_version":"0.10.0","subject":{"name":"sample-output","sha256":"a"*64},"claims":[{"check_id":"unit-tests","status":"PASS","evidence":["tests passed: 3"],"subject_sha256":"a"*64},{"check_id":"security-scan","status":"PASS","evidence":["scan report sha256: "+"b"*64],"subject_sha256":"a"*64}]}

def setup_keys(tmp_path):
    private=Ed25519PrivateKey.generate(); public=private.public_key()
    priv=tmp_path/'private.pem'; pub=tmp_path/'public.pem'
    priv.write_bytes(private.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
    pub.write_bytes(public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo))
    return priv,pub

def signed(tmp_path, payload=None):
    priv,pub=setup_keys(tmp_path); m=tmp_path/'manifest.json'; out=tmp_path/'signed.json'
    m.write_text(json.dumps(payload or manifest()))
    r=run('sign','--manifest',m,'--private-key',priv,'--output',out)
    assert r.returncode==0,r.stderr
    return priv,pub,out

def test_valid_signature_and_independent_policy_pass(tmp_path):
    _,pub,out=signed(tmp_path)
    v=run('verify','--signed',out,'--public-key',pub); assert v.returncode==0,v.stdout+v.stderr
    p=run('verify-policy','--signed',out,'--public-key',pub,'--required-check','unit-tests','--required-check','security-scan')
    assert p.returncode==0,p.stdout+p.stderr
    assert json.loads(p.stdout)['decision']=='PASS'

def test_tampered_payload_is_rejected(tmp_path):
    _,pub,out=signed(tmp_path); obj=json.loads(out.read_text()); obj['payload']['claims'][0]['status']='FAIL'; out.write_text(json.dumps(obj))
    r=run('verify','--signed',out,'--public-key',pub)
    assert r.returncode!=0
    assert 'digest mismatch' in r.stderr or 'signature verification failed' in r.stderr

def test_signature_valid_but_nonpassing_required_check_is_blocked(tmp_path):
    m=manifest(); m['claims'][1]['status']='BLOCKED'
    _,pub,out=signed(tmp_path,m)
    r=run('verify-policy','--signed',out,'--public-key',pub,'--required-check','unit-tests','--required-check','security-scan')
    assert r.returncode==2
    assert json.loads(r.stdout)['decision']=='BLOCKED'

def test_missing_required_check_is_blocked(tmp_path):
    _,pub,out=signed(tmp_path)
    r=run('verify-policy','--signed',out,'--public-key',pub,'--required-check','unit-tests','--required-check','live-gemini-smoke')
    assert r.returncode==2
    assert 'live-gemini-smoke' in json.loads(r.stdout)['missing_checks']

def test_pass_claim_without_evidence_cannot_be_signed(tmp_path):
    m=manifest(); m['claims'][0]['evidence']=[]
    priv,_=setup_keys(tmp_path); inp=tmp_path/'manifest.json'; out=tmp_path/'signed.json'; inp.write_text(json.dumps(m))
    r=run('sign','--manifest',inp,'--private-key',priv,'--output',out)
    assert r.returncode!=0
    assert not out.exists()


def test_claim_subject_hash_mismatch_cannot_be_signed(tmp_path):
    m=manifest(); m['claims'][0]['subject_sha256']='c'*64
    priv,_=setup_keys(tmp_path); inp=tmp_path/'manifest.json'; out=tmp_path/'signed.json'; inp.write_text(json.dumps(m))
    r=run('sign','--manifest',inp,'--private-key',priv,'--output',out)
    assert r.returncode!=0
    assert 'does not match manifest subject' in r.stderr

def test_empty_policy_cannot_pass(tmp_path):
    _,pub,out=signed(tmp_path)
    r=run('verify-policy','--signed',out,'--public-key',pub)
    assert r.returncode!=0
    assert 'at least one --required-check' in r.stderr
