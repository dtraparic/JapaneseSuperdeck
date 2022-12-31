import numpy as np
import pandas as pd

base = pd.read_csv('new_base.txt', '\t', header=None)  #(['kanji']+truc))
to_add = pd.read_csv('NEW_IMGS.txt', '\t', header=None)  #['kanji', 'keyword', 'better_story', 'stroke_count', 'heisig_index'])
min_to_add = to_add.iloc[:, [0,23,25]]
print(min_to_add)


truc = list(range(1, 29))
base.columns = ['kanji']+truc
min_to_add.columns = ['kanji', 'gif', 'png']




print(min_to_add)

fusion = pd.merge(base, min_to_add, on='kanji')
print(fusion)

fusion.to_csv('new_new_base.txt', sep='\t', header=False, index=False)
exit()
