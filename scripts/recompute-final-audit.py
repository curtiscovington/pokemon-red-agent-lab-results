import json,pathlib,hashlib,statistics,collections
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('batch_directory', type=pathlib.Path)
parser.add_argument('--output', type=pathlib.Path, default=pathlib.Path('audit-recomputed.json'))
args=parser.parse_args()
root=pathlib.Path(__file__).resolve().parents[1];p=args.batch_directory
f=json.loads((p/'confirmation-freeze.json').read_text());mismatch=[]
for n,h in f['sha256'].items():
 q=p/'source'/pathlib.Path(n).name if n.startswith('src/') or n.startswith('scripts/') else root/n
 if not q.exists() or hashlib.sha256(q.read_bytes()).hexdigest()!=h:mismatch.append(n)
print('FREEZE MISMATCH',mismatch)
rows=[]
for d in sorted(p.glob('[0-9][0-9]-*')):
 summary=json.loads((d/'summary.json').read_text());out=json.loads((d/'outcome-metrics.json').read_text());beh=json.loads((d/'behavior-metrics.json').read_text());firstbadge=None;badge_text=[];guide=0;brock=[];onix=[];reasons=collections.Counter();blocks=0;heals=0;lastparty=None;last=None;maxgap=0
 for line in (d/'events.jsonl').open():
  e=json.loads(line);t=e.get('elapsed') or 0;s=e.get('state');kind=e['type']
  if kind=='action_completed':
   reasons[e.get('result',{}).get('reason','primitive')]+=1
   if e.get('action')=='go:54-object-3':guide+=1
  if s:
   text=' '.join(s.get('interface',{}).get('text',[]));badge=s.get('player',{}).get('badges') or []
   if badge and firstbadge is None:firstbadge={'elapsed':t,'badges':badge,'text':text,'capture':e.get('capture'),'type':kind}
   if 'BOULDER' in text.upper() and (not badge_text or badge_text[-1]['text']!=text):badge_text.append({'elapsed':t,'text':text})
   if 'BROCK' in text.upper() and len(brock)<3:brock.append({'elapsed':t,'text':text})
   enemy=s.get('battle',{}).get('enemy',{})
   if s.get('battle',{}).get('in_battle') and enemy.get('species')=='Onix':onix.append({'elapsed':t,'hp':enemy.get('hp')})
   team=[(q.get('species_id'),q.get('level'),q.get('hp'),q.get('max_hp')) for q in s.get('party',[])]
   if lastparty and team and len(team)==len(lastparty) and all(a[:2]==b[:2] for a,b in zip(team,lastparty)) and any(a[2]>b[2] for a,b in zip(team,lastparty)) and s.get('map',{}).get('map_id') in (41,58):heals+=1
   if team:lastparty=team
   if kind=='observation':last={'map':s.get('map'),'party':s.get('party'),'badges':badge}
 row={'run':d.name,'recovery':summary['progress_control'],'seed':summary['seed'],'status':summary['status'],'first':out['first_observed_seconds'],'badge_evidence':firstbadge,'badge_dialogue':badge_text[:3],'brock_dialogue':brock,'onix_min_hp':min((x['hp'] for x in onix if x['hp'] is not None),default=None),'named_guide_calls':guide,'observed_center_hp_increases':heals,'navigation_reasons':dict(reasons),'interaction_block_decisions':beh['repeated_interaction_blocks'],'repeated_dialogue_pages':out['repeated_nonbattle_dialogue_pages'],'latency_median':summary['latency_p50_seconds'],'last':last,'errors':summary['errors'],'recoveries':summary['model_recoveries'],'resource_affected':summary['resource_affected']}
 rows.append(row)
 print(json.dumps({k:v for k,v in row.items() if k not in ['first','last','brock_dialogue','navigation_reasons']},ensure_ascii=False))
report={'batch':'20261013-105028-575ffb','freeze_mismatches':mismatch,'audit_scope':'Same streaming checks for all eight runs: badge state and dialogue, Brock/Onix encounter evidence, named gym-guide actions, center HP increases, navigation termination reasons, errors/recoveries and last main observation. Not exhaustive manual frame review. HP increases are observation events, not necessarily unique nurse visits; guide calls exclude direct confirm reopenings.','runs':rows}
args.output.write_text(json.dumps(report,indent=2)+'\n')
for treatment in [False,True]:
 rs=[r for r in rows if r['recovery']==treatment];print('GROUP',treatment,'median pewter',statistics.median(r['first']['pewter_reached'] for r in rs),'median inference',statistics.median(r['latency_median'] for r in rs),'guide calls',sum(r['named_guide_calls'] for r in rs))
