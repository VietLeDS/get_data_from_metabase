import os
lst = [f for f in os.listdir() if '.bat' in f and 'Meta' in f]
for _ in lst:
	os.remove(_)

lst = [f for f in os.listdir() if '.py' in f and 'Meta' in f]
for _ in lst:
	with open(_.replace('.py','.bat'), 'w') as f:
		f.write(f'TITLE {_.replace(".py", "")}\npython {_}\nPAUSE')