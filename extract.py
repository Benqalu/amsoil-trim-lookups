# Viscosity: 0W-30, 0W-40 (All TEMPS)
# 10W-30, 10W-40, 10W-50, 10W-60 (Above -20)
# 15W-30, 15W-40, 15W-50 (Above -15)
# 20W-40, 20W-50 (Above -5)
# 5W-30, 5W-40, 5W-50 (Above -25)
# Capacity: 8.5 quarts. . . (with filter)After refill check oil level.
# Torque: 22 ft/lbs (Oil Drain Plug)


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

	viscosity=re.findall(r'Viscosity:\s*(.+)',content)
	# capacity=re.findall('Capacity:((.|\r|\n)+)OIL FILTER')
	capacity=re.findall(r'[0-9\.]+ quarts\. \. \. .+',content)

	if len(viscosity)>0:
		viscosity=viscosity[0].strip()
	else:
		viscosity=''

	if len(capacity)>0:
		capacity='\n'.join(capacity)
	else:
		capacity=''

	rec[-1]=list(rec[-1])+[viscosity,capacity]

f.close()

rec=sorted(rec)

df = pd.DataFrame(rec,columns=['Year','Make','Model','Engine','Viscosity','Capacity'])

df.to_csv('lookups.csv',index=False)