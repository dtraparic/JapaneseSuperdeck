import pandas as pd
from pathlib import Path
import numpy as np
import pickle

cols = ['kanji', 'onyumi', 'kunyomi', 'nanori', 'english', 'francais', 'examples', 'JLPT', 'Jouyou', 'freq', 'comp',
        'strokes', 'radical', 'rad_num', 'rad_strokes', 'rad_read', 'trad', 'class', 'key', 'kooshii1', 'kooshii2',
        'RTKi', 'RTKChap', 'RTKStory', 'StrokesGIF', 'StrokesExtended', 'BetterRTKStory']

exclude_chars = '+=-＋＝ょゅ_' \
                'あかさたなはまやらわ' \
                'いきしちにひみりゐ' \
                'うくすつぬふむゆるん' \
                'えけせてねへめれゑ' \
                'おこそとのほもよろを' \
                'アカサタナハマヤラワ' \
                'イキシチニヒミリヰ' \
                'ウクスツヌフムユルン' \
                'エケセテネヘメレヱ' \
                'オコソトノホモヨロヲ'

# are_components_for_v2.pckl = comps scraped from pictured Stories IN ADDITION TO the 'components' field


"""Read csv"""

df = pd.read_csv('New_3_Without_prim_with_for_components.csv', sep='\t', header=None)
print(f'Shape of read csv : {df.shape}')

"""Gather cols of interest"""

kanjis = df.iloc[:, 0]
jlptn = df.iloc[:, 7]
kanjis_to_jlptn = dict(zip(kanjis, jlptn))
components_fields = df.iloc[:, 10]
picturedstories_fields = df.iloc[:, 27]

"""Scrap from 'components' field the characters only"""

components_all = []
for i, field in enumerate(components_fields):
    if isinstance(field, float):  # if is empty ? I think
        components_all.append([''])
        continue

    comp_strings = field.split(':')
    pure_comps = [c_string[-1] for c_string in comp_strings[:-1]]
    pure_comps = ''.join(pure_comps)
    components_all.append(pure_comps)

"""Scrap from 'RTKBetterStory' field the characters"""

for i, field in enumerate(picturedstories_fields):
    if isinstance(field, float):  # if is empty ? I think
        continue

    def keep_very_complex_char(string):
        buffer = ''
        for j, char in enumerate(string):
            if char in exclude_chars: continue
            if len(char.encode()) <= 2: continue
            else:
                try:
                    if string[j-1] == '(' and string[j+1] == ')':
                        buffer += char
                except IndexError:
                    continue
        return buffer

    comps_from_story = keep_very_complex_char(field)
    # x = ''.join(map(keep_very_complex_char, field))
    # x2 = ''.join(map(keep_very_complex_char, field))
    components_all[i] += comps_from_story
    components_all[i] = ''.join(set(components_all[i]))  # remove duplicate in str

print(f'Is composed from (direct child): {components_all}')

"""We have parent-link (is composed from) we want child-link (is component for)"""

# Save it once because it's calculus-expensive
RECOMPUTE = True
if RECOMPUTE:
    are_components_for = []
    for i, kanji in enumerate(kanjis):
        if i % 100 == 0: print(f'[{i}/{df.shape[0]}] Querying')
        is_component_for = ''
        for j, components_of_one in enumerate(components_all):
            if (kanji != kanjis[j]) and (kanji in components_of_one):
                is_component_for += kanjis[j]
        are_components_for.append(is_component_for)
    f = open('are_components_for_v2.pckl', 'wb')
    pickle.dump(are_components_for, f)
    f.close()
else:
    f = open('are_components_for_v2.pckl', 'rb')
    are_components_for = pickle.load(f)
    f.close()

print(f'Is component for : {are_components_for}')

kanjis_to_more_complex = dict(zip(kanjis, are_components_for))

"""Second-depth+ child-link"""
should_stop = False
i = 0
print(f'Size of initial tab : {len("".join(are_components_for))}')
old_tab = are_components_for
new_tab = []
while not should_stop:
    tab = []
    for j, is_component_for in enumerate(old_tab):
        is_component_for = ''.join(set(is_component_for))  # remove duplicate in str
        buffer = ''
        for single_comp in is_component_for:
            buffer += kanjis_to_more_complex[single_comp]
        buffer = ''.join(set(buffer))  # remove duplicate in str
        tab.append(buffer)

    print(f'[{i}] single additionnal pass only is component for : {tab}')
    new_tab = [a + b for a, b in zip(old_tab, tab)]
    new_tab = [''.join(set(a)) for a in new_tab]
    print(f'[{i}] pass added is component for : {new_tab}')
    should_stop = np.array_equal(len("".join(new_tab)), len("".join(old_tab)))
    old_tab = new_tab
    i += 1

    print(f'Size of new_tab {len("".join(new_tab))}')
    print(f'{i} iterations done.')

# exit()


are_components_for_jlpts = []

are_components_for = new_tab  # DESACTIVER SI BESOIN
for i, is_component_for in enumerate(are_components_for):
    is_component_for_jlpts = ''
    for char in is_component_for:
        is_component_for_jlpts += str(kanjis_to_jlptn[char])
    are_components_for_jlpts.append(is_component_for_jlpts)

print(are_components_for_jlpts)

are_comp_for_grouped_jlpt = []
for i, is_component_for_jlpts in enumerate(are_components_for_jlpts):
    count_N5 = is_component_for_jlpts.count('5')
    count_N4 = is_component_for_jlpts.count('4')
    count_N3 = is_component_for_jlpts.count('3')
    count_N2 = is_component_for_jlpts.count('2')
    count_N1 = is_component_for_jlpts.count('1')
    count_N0 = is_component_for_jlpts.count('0')

    counts = [count_N5, count_N4, count_N3, count_N2, count_N1, count_N0]
    label_groups = ['N5', 'N4', 'N3', 'N2', 'N1', 'N0']
    # is_comp_for_grouped_jlpt = f'{count_N5} N5, {count_N4} N4, {count_N3} N3, {count_N2} N2, {count_N1} N1, {count_N0} N0'
    growing_string = ''

    assert len(counts) == len(label_groups)
    for j, count in enumerate(counts):
        if count > 0:
            if len(growing_string):
                growing_string += ', '
            growing_string += f'{count} {label_groups[j]}'

    if len(growing_string) == 0:
        growing_string = 'none'

    are_comp_for_grouped_jlpt.append(growing_string)

are_comp_for_grouped_jlpt = np.array(are_comp_for_grouped_jlpt)
print(are_comp_for_grouped_jlpt.shape)
print(are_comp_for_grouped_jlpt[:10])

df_comp_for_kanjis = pd.DataFrame(are_components_for)
df_comp_for_jlpt = pd.DataFrame(are_comp_for_grouped_jlpt)

"""Ici c'est en mettant aussi tous are_components_for, mais il peut y en avoir jsais pas 300 par kanji de base donc bof"""
# frames = [df, df_comp_for_kanjis, df_comp_for_jlpt]
# result = pd.concat(frames, axis=1)
# result.to_csv('New_Without_prim_with_for_components.txt', sep='\t', header=False, index=False)

frames = [df, df_comp_for_jlpt]
result = pd.concat(frames, axis=1)
result.to_csv('New_4_Without_prim_with_for_components.csv', sep='\t', header=False, index=False)

# Pourquoi Arbre, Not Yet, Extremity et Vache ont exactement le même score ?
# Je pense que c'est parce que pour Arbre/Not Yet/Extremity, c'est les memes histoires donc ils sont interdépendants
# et ca fout la merde, et plein de dépendances cycliques
# Faudrait que je dise qu'un truc avec un RTKIndex supérieur, ne peut pas être primitive d'un RTKindex inférieur
