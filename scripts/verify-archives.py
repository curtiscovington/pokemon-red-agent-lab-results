"""Check published archives against original member hashes and run durations."""
from pathlib import Path
import hashlib,json,tarfile
root=Path(__file__).resolve().parents[1]
index=json.loads((root/'batch-index.json').read_text())
hashes=json.loads((root/'archive-members-sha256.json').read_text())
seen=set(); completed=0; interrupted=0; elapsed=0
for batch in index:
    path=root/batch['archive']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==batch['archive_sha256'],path
    with tarfile.open(path,'r:gz') as archive:
        for member in archive:
            assert member.isfile() and not member.name.startswith('/') and '..' not in Path(member.name).parts
            key=batch['version']+'/'+member.name
            assert key not in seen,key
            seen.add(key)
            data=archive.extractfile(member).read()
            assert hashlib.sha256(data).hexdigest()==hashes[key],key
            if member.name.endswith('/events.jsonl'):
                for line in data.splitlines():json.loads(line)
            if member.name.endswith('/summary.json'):
                summary=json.loads(data)
                completed+=summary['status']=='completed'
                interrupted+=summary['status']=='interrupted'
                elapsed+=summary['elapsed_seconds']
    print(batch['version'],'verified')
assert seen==set(hashes)
assert (completed,interrupted)==(40,1)
print(f'{completed} completed runs, {interrupted} interrupted; {elapsed/3600:.4f} gameplay hours. All hashes and event JSON valid.')
