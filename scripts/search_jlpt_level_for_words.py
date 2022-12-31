import pandas as pd
from jisho_api.word import Word
from jisho_api.kanji import Kanji
from jisho_api.sentence import Sentence
from jisho_api.tokenize import Tokens
import random

"""Get N random kanjis"""
get_random_from_true_set = False
if get_random_from_true_set:
    i_rand = random.sample(range(0, 3000), 10)
    print(i_rand)
    df = pd.read_csv('2022-11-06 output superdeck words replaced.csv', sep='\t')
    kanjis = list(df.iloc[i_rand, 0])
    print(kanjis)

"""Define kanjis"""
i_rand = [2580, 788, 667, 630, 93, 1955, 2121, 2871, 2480, 1686]
kanjis = ['槃', '奨', '悟', '店', '丁', '講', '懇', '歎', '藷', '鋳']
kanjis = ['丁']

# r = Word.request('槃')
# # r = Word.request('誰')
r = Word.request('夢')
print(r)
print(len(r.data), r.data)
print('Les wordconfig')
print(r.data[0])
print(r.data[1])
print(r.data[2])
print(r.data[3])
print(r.data[4])
print(r.data[5])
print(r.data[6])
print(r.data[7])
print(r.data[8])
print(r.data[9])
print()
print(r.data[0])
print()
print(r.data[0].senses)
print(r.data[0].slug)
exit()

print("All slugs : ")
growing_dic_common_words = {}
growing_dic_uncommon_words = {}

for kanji in kanjis:
    r = Word.request(kanji)
    for i_word in range(len(r.data)):
        word = r.data[i_word]
        if len(word.slug) > 10:
            print(f"{kanji}: Word without reading, Skipped")
        else:
            jlpt = [jlpt_str[-1] for jlpt_str in word.jlpt]
            print(jlpt)
            commonest_reading_i = word.jlpt
            # growing_dic_common_words[kanji] = {'jlpt': }
            print(kanji, word.slug, word.jlpt, word.is_common)
        # print(f'')

# Un output bizarre
# [2580, 788, 667, 630, 93, 1955, 2121, 2871, 2480, 1686]
# ['槃', '奨', '悟', '店', '丁', '講', '懇', '歎', '藷', '鋳']
# All slugs :
# 5186a019d5dda7b2c608c0e6 [] None
# 奨学金 ['jlpt-n3'] True
# 勧める ['jlpt-n3'] True
# 奨励 ['jlpt-n1'] True
# 勧め ['jlpt-n1'] True
# 奨励賞 [] False
# 奨学 [] True
# 奨学生 [] False
# 奨学資金 [] False
# 奨励金 [] False
# 奨学金制度 [] False
# 5186998ed5dda7b2c605a57a [] None
# 51869851d5dda7b2c605117a [] None


# for kanji in kanjis:
