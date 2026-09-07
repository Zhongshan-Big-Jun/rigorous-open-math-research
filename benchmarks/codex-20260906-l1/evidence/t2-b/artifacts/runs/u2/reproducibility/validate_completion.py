"""Deterministic validation confined to this run's proof package; no git/network."""
from pathlib import Path
import hashlib,json,re
r=Path(__file__).resolve().parents[1]
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m_path=r/'completion_manifest.json'
m=json.loads(m_path.read_text())
failures=[]
for name,d in [(k,m[k]) for k in ('contract','obligation_graph','candidate_proof')]+[('dependency',d) for d in m['dependencies']]:
    p=(r/d['path']).resolve()
    if not p.is_relative_to(r.parents[1]): failures.append(name+': outside task workspace')
    elif not p.is_file() or h(p)!=d['sha256']: failures.append(name+': hash mismatch')
g=json.loads((r/m['obligation_graph']['path']).read_text())
roots=m['root_obligations']
if [x['id'] for x in roots]!=g['root_obligations']: failures.append('root array mismatch')
for d in roots:
    if d['status']!='CLOSED': failures.append(d['id']+': not closed')
    path,anchor=d['proof_anchor'].split('#',1)
    if 'id="'+anchor+'"' not in (r/path).read_text(): failures.append(d['id']+': missing proof anchor')
a_path=r/'completion_audit.json'
if a_path.exists():
    a=json.loads(a_path.read_text())
    if a['audited_manifest_sha256']!=h(m_path): failures.append('audit manifest mismatch')
    if a['candidate_author_id']!=m['candidate_author_id']: failures.append('audit author mismatch')
    if a['reviewer_id']==m['candidate_author_id']: failures.append('reviewer not independent')
    if a['verdict']!='PASS' or a['load_bearing_gaps']: failures.append('audit has not passed with zero gaps')
    if a['reviewed_at']<m['frozen_at']: failures.append('audit timestamp precedes freeze')
    audit_status=a['verdict']
else:
    failures.append('independent audit pending')
    audit_status='PENDING'
result={'check':'confined completion manifest/root/anchor/independence validation','verdict':'PASS' if not failures else 'PENDING_OR_FAIL','audit_status':audit_status,'failures':failures,'manifest_sha256':h(m_path),'proof_sha256':m['candidate_proof']['sha256']}
(r/'deterministic_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(bool(failures))
