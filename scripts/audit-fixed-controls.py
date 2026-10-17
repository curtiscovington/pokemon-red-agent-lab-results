"""Uniform evidence audit of every fixed-controls run; stdlib only."""
import argparse, json, collections, statistics
from pathlib import Path

def audit(batch):
 rows=[]
 for p in sorted(batch.glob('[0-9][0-9]-*')):
  summary=json.loads((p/'summary.json').read_text());milestones=json.loads((p/'outcome-metrics.json').read_text())['first_observed_seconds']
  counts=collections.Counter();reasons=collections.Counter();moves=collections.Counter();first=None;awards=[];errors=[];samples=[];offered=[];lastparty=None;contexts=collections.Counter();brock=False;onix=False;guide=0;hp_increases=0;lastcontext={};request_n=0
  for line,l in enumerate((p/'events.jsonl').open(),1):
   e=json.loads(l);t=e.get('elapsed');kind=e['type']
   if t is None or not 0<=t<=3600:continue
   if kind=='request':
    request_n+=1;r=e['request'];offered=r['format']['properties']['action']['enum'];text=r['messages'][0]['content'];c=json.loads(text[text.index('{"state":'):]);s=c['state'];lastcontext={'map':s['map']['map_name'],'objective':c.get('objective',{}).get('id'),'interface':s.get('interface',{}).get('kind'),'offered':len(offered)};contexts[(lastcontext['map'],lastcontext['objective'])]+=1
    if request_n==1 or request_n%100==0:samples.append({'line':line,'seconds':t,**lastcontext})
   if kind=='response':
    try:
     a=json.loads(e['response']['message']['content'])['action'];counts['outside_enum']+=a not in offered
     counts['route_target_unavailable']+=e['response'].get('policy_rule')=='route_target_unavailable'
    except (ValueError,KeyError,TypeError):counts['malformed']+=1
   if kind=='action_completed':
    a=e['action'];reasons[e.get('result',{}).get('reason','primitive')]+=1
    guide+=a=='go:54-object-3'
    if a.startswith('use:'):moves[a]+=1
   if kind in ('error','failure','stale_action_discarded','late_response_ignored'):
    counts[kind]+=1
    if kind in ('error','failure'):errors.append({'line':line,'seconds':t,'error':e.get('error')})
   s=e.get('state') or e.get('result',{}).get('state_after') or {}
   if not s:continue
   badges=s.get('player',{}).get('badges',[]);text=' '.join(s.get('interface',{}).get('text',[]))
   if 'Boulder' in badges and first is None:first={'line':line,'seconds':t}
   if ('BOULDER' in text.upper() and ('RECEIVED' in text.upper() or 'VICTORY' in text.upper())) and len(awards)<3:awards.append({'line':line,'seconds':t,'text':text})
   battle=s.get('battle',{});enemy=battle.get('enemy',{}).get('species');mid=s.get('map',{}).get('map_id')
   brock|=mid==54 and battle.get('in_battle',False) and enemy=='Geodude';onix|=mid==54 and battle.get('in_battle',False) and enemy=='Onix'
   party=[(x.get('species_id'),x.get('level'),x.get('hp')) for x in s.get('party',[])]
   if lastparty and len(party)==len(lastparty) and mid in (41,58) and all(a[:2]==b[:2] for a,b in zip(party,lastparty)) and any(a[2]>b[2] for a,b in zip(party,lastparty)):hp_increases+=1
   if party:lastparty=party
  final=json.loads((p/'final-observation.json').read_text())['player']['badges'];assert bool(first)==('Boulder' in final)==('first_badge' in milestones)
  rows.append({'run':p.name,'policy':summary['policy'],'milestones':milestones,'badge':first,'award_dialogue':awards,'final_badges':final,'counts':dict(counts),'navigation_reasons':dict(reasons),'named_move_actions':dict(moves),'brock_geodude_seen':brock,'onix_seen':onix,'guide_calls':guide,'center_hp_increases':hp_increases,'errors':errors,'fixed_samples':samples,'top_request_contexts':[{'map':k[0],'objective':k[1],'requests':v} for k,v in contexts.most_common(3)]})
 return {'batch':batch.name,'scope':'Same full-log checks for all45 runs: badge state/award dialogue, offered-action legality, Brock/Onix evidence, named moves/guide calls, observed center HP increases, navigation reasons, errors and deterministic first/every100th request samples. Not exhaustive manual review of every frame. Existing policy-audit manual_review flags remain untouched; this is a separate uniform log audit.','runs':rows}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('batch',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.write_text(json.dumps(audit(a.batch),indent=2)+'\n')
