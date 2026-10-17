"""Allowlisted v2.25 evidence export; excludes ROMs/saves/resource/service logs."""
import argparse,hashlib,json,tarfile,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('batch',type=Path);a=p.parse_args();root=Path(__file__).resolve().parents[1];out=root/'batches/v2.25';out.mkdir(parents=True,exist_ok=True);index=[]
def archive(name,files):
 path=out/name;members={}
 with tarfile.open(path,'w:gz',compresslevel=6) as tar:
  for file in sorted(files):
   rel=str(file.relative_to(a.batch));tar.add(file,arcname=rel,recursive=False);members[rel]=hashlib.sha256(file.read_bytes()).hexdigest()
 index.append({'archive':str(path.relative_to(root)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'members':members})
for run in sorted(a.batch.glob('[0-9][0-9]-*')):
 names=['events.jsonl','summary.json','outcome-metrics.json','behavior-metrics.json','policy-audit.json','manifest.json','final-observation.json','final.png']
 files=[run/n for n in names if (run/n).is_file()]+list((run/'frames').glob('*.png'))
 archive(run.name+'.tar.gz',files)
 dest=out/'runs'/run.name;dest.mkdir(parents=True,exist_ok=True)
 for n in names:
  if n not in ('events.jsonl','final.png') and (run/n).exists():shutil.copyfile(run/n,dest/n)
files=[a.batch/n for n in ['manifest.json','status.json','REPORT.md','confirmation-freeze.json'] if (a.batch/n).exists()]
files+=list((a.batch/'source').glob('*.py'))+list((a.batch/'source').glob('combat_data.json'))
archive('source-and-manifest.tar.gz',files)
(out/'archive-index.json').write_text(json.dumps(index,indent=2)+'\n')
print('Exported',len(index),'archives',sum((root/i['archive']).stat().st_size for i in index)//1048576,'MiB')
