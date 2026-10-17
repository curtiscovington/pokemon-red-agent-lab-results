import hashlib,json,tarfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
index=json.loads((root/'batches/v2.25/archive-index.json').read_text());runs=0
for entry in index:
 p=root/entry['archive'];assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256']
 with tarfile.open(p) as tar:
  names=[]
  for m in tar:
   assert m.isfile() and not Path(m.name).is_absolute() and '..' not in Path(m.name).parts
   assert not m.name.endswith(('.gb','.state','.safetensors','.gguf'))
   data=tar.extractfile(m).read();assert hashlib.sha256(data).hexdigest()==entry['members'][m.name];names.append(m.name)
   if m.name.endswith('/summary.json'):assert json.loads(data)['status']=='completed';runs+=1
  assert set(names)==set(entry['members'])
assert runs==45
print('All46 archives and member hashes verified;45 completed runs; no ROM/save/model binaries')
