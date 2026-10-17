"""Pre-specified fixed-batch analysis; refuses incomplete/affected runs."""
import argparse
import json
import math
from pathlib import Path


def wilson(k,n):
    z=1.959963984540054;p=k/n;den=1+z*z/n
    center=(p+z*z/(2*n))/den
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [max(0,center-half), min(1,center+half)]


def fisher(a,b,c,d):
    n=a+b;m=c+d;s=a+c
    def weight(x):return math.comb(n,x)*math.comb(m,s-x)
    observed=weight(a)
    return min(1,sum(weight(x) for x in range(max(0,s-m),min(n,s)+1) if weight(x)<=observed)/math.comb(n+m,s))


def analyze(folder):
    status=json.loads((folder/'status.json').read_text())
    rows=status['results']
    if status['stage']!='complete' or len(rows)!=45 or any(r['status']!='completed' or r.get('resource_affected') for r in rows):
        raise ValueError('Requires all45 completed unaffected runs; audit infrastructure failures separately')
    arms={}
    for policy in ('random','scripted','reactive'):
        selected=[r for r in rows if r['policy']==policy]
        if len(selected)!=15:raise ValueError('Expected15 per arm')
        audits=[json.loads((folder/r['run_id']/'policy-audit.json').read_text()) for r in selected]
        times=[a['first_badge']['elapsed'] if a.get('first_badge') else 3600 for a in audits]
        wins=sum(a.get('first_badge') is not None for a in audits)
        milestones={}
        for milestone in sorted(set(k for a in audits for k in a['milestones'])):
            event_times=[a['milestones'].get(milestone) for a in audits]
            event_times=[t if t is not None and 0<=t<=3600 else None for t in event_times]
            milestones[milestone]={'completed':sum(t is not None for t in event_times),'n':15,
                'restricted_mean_seconds_3600':sum(t if t is not None else 3600 for t in event_times)/15}
        arms[policy]={'badges':wins,'n':15,'wilson95':wilson(wins,15),
            'badge_restricted_mean_seconds_3600':sum(times)/15,'milestones':milestones,
            'manual_reviews_pending':sum(a.get('manual_review')!='complete' for a in audits)}
    a=arms['reactive']['badges'];b=arms['scripted']['badges']
    return {'arms':arms,'primary_model_vs_script_fisher_two_sided_p':fisher(a,15-a,b,15-b),
        'alpha':.05,'interpretation':'Primary test assumes independent repeated trials; policy seeds do not reseed game RNG. Pending trace review precludes final publication. Secondary milestones exploratory; unreached are censored at3600.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('batch',type=Path);args=parser.parse_args()
    print(json.dumps(analyze(args.batch),indent=2))
