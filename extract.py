import os, re
import pandas as pd

f=open('./record/records.txt')
rec=[]
for line in f:
	info=eval(line)

	# if tuple(list(info)[:3])!=('2010','Audi','R8'):
	# 	continue

	rec.append(info)

	s = '%s %s %s %s'%rec[-1]
	s = re.sub('[\(\)\\\,\.\;\:\'\"\/\s]','_',s)

	g=open(f'./record/{s}.txt')
	content=''.join(g.readlines())
	g.close()

	res_v=re.findall('Viscosity:\s*([^\n]+)\n',content)
	res_c=re.findall('Capacity:\s*([^\n]+)\n',content)
	if len(res_v)==0:
		res_v='N/A'
	else:
		res_v=res_v[0]
	if len(res_c)==0:
		res_c='N/A'
	else:
		res_c=res_c[0]
	rec[-1]=list(rec[-1])+[res_v,res_c]

f.close()

rec=sorted(rec)

df = pd.DataFrame(rec,columns=['Year','Make','Model','Engine','Viscosity','Capacity'])

df.to_csv('lookups.csv',index=False)