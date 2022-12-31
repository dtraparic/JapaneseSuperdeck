from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import numpy as np
import pandas as pd

options = Options()
options.binary_location = r"D:/MesProgrammes/Firefox Developper Edition/firefox.exe"

driver = webdriver.Firefox(options=options)

# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element(By.NAME, "q")  # GET this: <input id="id-search-field" name="q" type="search">
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()

driver.get('https://jlptsensei.com/jlpt-n5-grammar-list/')
elem = driver.find_elements(By.CLASS_NAME, "jl-row")
elem2 = driver.find_elements(By.CSS_SELECTOR, '.jl-row')

print(elem)
print(len(elem))
print(elem2)
print(len(elem2))

keywords = driver.find_elements(By.CSS_SELECTOR, '.jl-row > td:nth-child(2) > a')
japs = driver.find_elements(By.CSS_SELECTOR, '.jl-row > td:nth-child(3) > a')
meanings = driver.find_elements(By.CSS_SELECTOR, '.jl-row > td:nth-child(4)')

list_tensor = []
array_links = []

for i in range(len(keywords)):
    keyword = keywords[i].get_attribute("innerHTML")
    jap = japs[i].get_attribute("innerHTML")
    meaning = meanings[i].get_attribute("innerHTML")

    link = keywords[i].get_attribute("href")

    line = [keyword, jap, meaning]
    list_tensor.append(line)
    array_links.append(link)

tensor = np.array(list_tensor)
print(tensor)
print(tensor.shape)

print(array_links)
print(len(array_links))

static_cols = ['rule_roma', 'rule_jap', 'meaning']
df_rules = pd.DataFrame(list_tensor, columns=static_cols)
print('Shape of df rules:', df_rules.shape)
print(df_rules)

usages = []
all_rules_examples_kanji = []
all_rules_examples_kana = []
all_rules_examples_en = []

for i, link in enumerate(array_links):

    EARLY_STOP = False
    if EARLY_STOP and i == 5:
        break

    exemples = []
    driver.get(link)

    usage_elmt = driver.find_element(By.CSS_SELECTOR, "#usage table")

    example_kanji_elmts = driver.find_elements(By.CSS_SELECTOR, "#examples .example-main>p")
    example_kana_elmts = driver.find_elements(By.CSS_SELECTOR, 'div[id^="example_"][id$="_ja"]')
    example_en_elmts = driver.find_elements(By.CSS_SELECTOR, 'div[id^="example_"][id$="_en"]')

    if len(example_kanji_elmts) == len(example_kana_elmts) == len(example_en_elmts) == 0:
        example_kanji_elmts = driver.find_elements(By.CSS_SELECTOR, ".ex-block .ja")
        example_kana_elmts = []
        example_en_elmts = driver.find_elements(By.CSS_SELECTOR, '.ex-block .gram-honyaku')

    usage = usage_elmt.get_attribute("outerHTML")

    examples_kanji = [elmt.get_attribute('innerHTML') for elmt in example_kanji_elmts]
    examples_kana = [elmt.get_attribute('innerText') for elmt in example_kana_elmts]
    examples_en = [elmt.get_attribute('innerText') for elmt in example_en_elmts]

    # DEBUG = True
    # if DEBUG:
    #     assert len(examples_kanji) == len(examples_kana) == len(examples_en)
    #     print(f'Rule [{i}] nb: {len(examples_kanji)}, {examples_kanji}')
    #     # print(f'Rule [{i}] nb: {len(examples_kana)}, {examples_kana}')
    #     # print(f'Rule [{i}] nb: {len(examples_en)}, {examples_en}')

    DEBUG_TABLE = False

    if DEBUG_TABLE: print("Table of how-to-use:", usage)
    print(f'Rule [{i}] Nb ex in kanjis: {len(example_kanji_elmts)}, \t Nb ex kana: {len(example_kana_elmts)}, \t Nb ex in EN.: {len(example_en_elmts)}')

    usages.append([usage, '5'])
    all_rules_examples_kanji.append(examples_kanji)
    all_rules_examples_kana.append(examples_kana)
    all_rules_examples_en.append(examples_en)

# TODO
#  Remanier exKanji1 exKana1 exEN1 puis 2 puis etc. C'EST FAIT
#  Peut-être choper les .block-ex, surtout si aucun exemple

# df = pd.DataFrame([all_rules_examples_kanji, all_rules_examples_kana, all_rules_examples_en])  # marche pas
# df = pd.DataFrame([all_rules_examples_kanji + all_rules_examples_kana + all_rules_examples_en])  # marche pas

cols_ex_kanji = [f'Example {i+1} Kanji' for i in range(10)]
cols_ex_kana = [f'Example {i+1} Kana' for i in range(10)]
cols_ex_en = [f'Example {i+1} English' for i in range(10)]

df0 = pd.DataFrame(usages, columns=['Usage', 'JLPT N'])
df1 = pd.DataFrame(all_rules_examples_kanji, columns=cols_ex_kanji)  # marche , mais y a pas tout
df2 = pd.DataFrame(all_rules_examples_kana, columns=cols_ex_kana)  # marche , mais y a pas tout
df3 = pd.DataFrame(all_rules_examples_en, columns=cols_ex_en)  # marche , mais y a pas tout

print('shape of df0:', df0.shape)
print('shape of df1:', df1.shape)
print('shape of df2:', df2.shape)
print('shape of df3:', df3.shape)

# tensor = np.array(all_rules_examples_kanji)  # marche pas, pas meme taille
df = df_rules.join(df0)
print('0Shape after join of df : ', df.shape)
df = df.join(df1)
print('1Shape after join of df : ', df.shape)
df = df.join(df2)
print('2Shape after join of df : ', df.shape)
df = df.join(df3)
print('3Shape after join of df : ', df.shape)
# mtn je join les tables 1 2 3

reindexed_cols = static_cols
reindexed_cols.append('Usage')
reindexed_cols.append('JLPT N')
for i in range(10):
    reindexed_cols.append(f'Example {i+1} Kanji')
    reindexed_cols.append(f'Example {i+1} Kana')
    reindexed_cols.append(f'Example {i+1} English')

df = df.reindex(columns=reindexed_cols)

print(df)
# print(tensor.shape)

# J'ai rajouté à la main le champs JLPT N : 5

df.to_csv('test.csv', sep="\t")

# TODO
#   Maintenant choper le span qui colorie en rouge dans les exemples kanjis la notion
#   Ok ca marche bien t'as super bien fait les exemples fix 100 fois mais par contre y a ni ID de la regle, ni meaning ni ecriture de la regle en jap

# """## Format string in field"""
#
# format_all_examples_one_rule = ''
# for i in range(len(all_rules_examples_kanji)):
#     one_example_paragraph = ''
#     for j in range(len(all_rules_examples_kanji[i])):
#         one_example_paragraph += all_rules_examples_kanji[i][j]+'\n'
#         one_example_paragraph += all_rules_examples_kana[i][j]+'\n'
#         print('salut')

    # format_all_examples_one_rule += one_example_paragraph+'\n'



driver.close()
# https://jlptsensei.com/jlpt-n5-grammar-list/
# https://jlptsensei.com/learn-japanese-grammar/%e3%81%a1%e3%82%83%e3%81%84%e3%81%91%e3%81%aa%e3%81%84-%e3%81%98%e3%82%83%e3%81%84%e3%81%91%e3%81%aa%e3%81%84-cha-ikenai-ja-dame/