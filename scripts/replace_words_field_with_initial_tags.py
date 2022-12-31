import pandas as pd
import numpy as np

df_superdeck = pd.read_csv('2022-11-06 Japanese Superdeck__Heisig RTK Remembering the Kanjis.txt', header=None, sep='\t')
df_allinone = pd.read_csv('original All In One Deck.txt', sep='\t', header=None)

print(df_superdeck.iloc[0, 6])
print(df_allinone.iloc[0, 5])

df_superdeck_wo_prim = df_superdeck.iloc[:3000, :]
# print(df_superdeck_wo_prim)
better_words = df_allinone.iloc[:, 5]


def is_it_all_aligned(df1, df2):
    list_kanji1 = list(df1.iloc[:,0])
    list_kanji2 = list(df2.iloc[:,0])

    return all(np.array(list_kanji1) == list_kanji2)

assert is_it_all_aligned(df_superdeck_wo_prim, df_allinone)

# df_superdeck_wo_prim.loc[6] = better_words
# df = df.assign(B=df1['E'])
# print()

# df_superdeck_wo_prim.iloc[:, 6] = list(better_words)

"""Je bruteforce le deep copy parce que ca commence a faire chier que rien ne marche
en cherchant dataframe replace a col"""
new_growing_list_to_df = []
for i in range(df_superdeck_wo_prim.shape[1]):
    if i == 6:
        new_growing_list_to_df.append(list(better_words))
    else:
        new_growing_list_to_df.append(list(df_superdeck_wo_prim.iloc[:, i]))


"""
Demo : 
>>> salut = [['A', 'B', 'C'], [1, 2, 3], ['?', '!', '%']]
>>> list(set(zip(*salut)))
"""

new_growing_list_to_df = zip(*new_growing_list_to_df)

new_df = pd.DataFrame(new_growing_list_to_df, index=None)


print('\n')
print(df_superdeck.iloc[0, 6])
print(df_allinone.iloc[0, 5])
print(new_df.iloc[0, 6])

print(new_df.iloc[:, 0:10])
print(new_df.iloc[0:10, :])
new_df.to_csv('2022-11-06 output superdeck words replaced.csv', sep='\t', header=False, index=False)


# FIXME ca marche pas ptn