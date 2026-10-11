#!/usr/bin/env python3
"""Build an in-toto Statement v1 with 3 subjects (sha256 of fixture files) and the D5 plan-approval fields.
Usage: python3 -I build_statement.py <fixtures_dir> <out_statement.json>"""
import hashlib, json, os, sys
fx, out = sys.argv[1], sys.argv[2]
names = ["grant.json", "plan-manifest.json", "tree.txt"]
def sha(p):
    with open(p, "rb") as f: return hashlib.sha256(f.read()).hexdigest()
subjects = [{"name": n, "digest": {"sha256": sha(os.path.join(fx, n))}} for n in names]
grant = json.load(open(os.path.join(fx, "grant.json")))
stmt = {
  "_type": "https://in-toto.io/Statement/v1",
  "subject": subjects,
  "predicateType": "https://example.invalid/govern/plan-approval/v1",
  "predicate": {
    "grantId": grant["grantId"],
    "Subject": grant["subject"],
    "BaseRef": grant["baseRef"],
    "presentedDigest": "sha256:" + hashlib.sha256(b"spike-rendering-placeholder").hexdigest(),
    "rendererVersion": "spike-0",
    "policyDigest": "sha256:" + hashlib.sha256(b"spike-policy-placeholder").hexdigest(),
    "assurance": "unassured",
    "host": "spike",
    "kIndex": 1
  }
}
with open(out, "w") as f: json.dump(stmt, f, indent=2, sort_keys=True); f.write("\n")
for s in subjects: print(s["digest"]["sha256"], s["name"])
