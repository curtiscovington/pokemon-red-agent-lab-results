from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
root=Path(__file__).resolve().parents[2]
rows=list(csv.DictReader((root/'results/fixed-controls/runs.csv').open()))
fig,axes=plt.subplots(3,1,figsize=(8,6.6),sharex=True)
colors={'random':'#777777','scripted':'#257657','reactive':'#455cbb'}
for ax,(field,title) in zip(axes,[('pewter_seconds','Reach Pewter'),('gym_seconds','Enter Gym'),('badge_seconds','Earn Badge')]):
 for y,policy in enumerate(['random','scripted','reactive']):
  rs=[r for r in rows if r['policy']==policy]
  for i,r in enumerate(rs):
   reached=bool(r[field]);t=float(r[field])/60 if reached else 60
   ax.scatter(t,y+(i-7)*.035,color=colors[policy],marker='o' if reached else 'x',s=23,linewidths=1)
 ax.set_yticks([0,1,2],['Random','Script','Model']);ax.set_title(title,loc='left',fontsize=11)
 ax.set_xlim(0,63);ax.set_ylim(2.4,-.4);ax.grid(axis='x',alpha=.2);ax.spines[['top','right']].set_visible(False)
axes[-1].set_xlabel('Minutes from bedroom start')
fig.suptitle('Same controls, 15 one-hour runs per policy',fontsize=13)
fig.legend(handles=[
 Line2D([], [], color='#333333', marker='o', linestyle='None', label='Milestone reached'),
 Line2D([], [], color='#333333', marker='x', linestyle='None', label='Not reached within 60 min'),
], loc='upper center', bbox_to_anchor=(.5, .945), ncol=2, frameon=False, fontsize=11)
fig.subplots_adjust(top=.85, bottom=.09, left=.1, right=.98, hspace=.4)
fig.savefig(root/'images/fixed-controls/milestones.png',dpi=180)
