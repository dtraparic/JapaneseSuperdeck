import numpy as np
import pandas as pd

truc = list(range(1, 28))
base = pd.read_csv('base.txt', '\t', header=None)#(['kanji']+truc))
to_add = pd.read_csv('imaged_stories.txt', '\t', header=None)#['kanji', 'keyword', 'better_story', 'stroke_count', 'heisig_index'])
min_to_add = to_add.iloc[:, [0,2]]

base.columns = ['kanji']+truc
min_to_add.columns = ['kanji', 'better_story']




print(min_to_add)

fusion = pd.merge(base, min_to_add, on='kanji')
print(fusion)

fusion.to_csv('new_base.txt', sep='\t', header=False, index=False)
exit()

# base = base.sort_values(base.columns[21])
# to_add = to_add.sort_values(to_add.columns[4])
# left, right = base.align(to_add, axis=0, level=0)
# truc = base.join(to_add, on=base.columns[0])
# print(left.iloc[100:110, :5])
# print("EHO")
# print(right.iloc[100:110, :5])

# print(base.iloc[:, 21]) # col RTK Index
# print(to_add.iloc[:, 4]) # col RTK Index

print("SEPARER")
print(base.iloc[:, 23])
print("SEPARER")
print(list(to_add.iloc[:5, 2]))  # col better RTK_Story
print("SEPARER")
# print(to_add)
exit()

all_kanjis_1 = list(base.iloc[:, 0])
all_kanjis_2 = list(to_add.iloc[:, 0])

print(len(all_kanjis_1))
print(len(all_kanjis_2))

all_imaged_stories = list(to_add.iloc[:, 2])
all_imaged_stories += [''] * (3000 - len(all_imaged_stories))
base.insert(loc=len(base.columns), column="better_story", value=all_imaged_stories)

print(base.iloc[2])
