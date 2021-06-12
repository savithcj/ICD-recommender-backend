import re
import pandas as pd
import xml.etree.ElementTree as ET
from collections import defaultdict


def inclusion_terms_clean(text):
    text = re.sub('\(.*?\)', '', str(text))  # Remove any words within ()
    text = re.sub('\s+', ' ', text).strip()  # replace multiple spaces with single and remove leading and trailing space
    text = re.sub('\)', '', text).strip()
    return text


def getKeywordTerms():
    icd10_cm = ET.parse('data/icd10cm_index_2020.xml')
    print("Reading keyword terms from file...")
    output_list = {}
    i = 1

    for node in icd10_cm.iter():
        # update the main term
        if node.tag == 'mainTerm':
            main = " ".join(node.find('title').itertext())
            main_clean = inclusion_terms_clean(main)

            code_main = node.findtext('code')
            if node.findtext('code') is not None:
                output_list[i] = {'icd_code': code_main,
                                  'term_list': [main],
                                  'level_0': main_clean}
                i += 1
        if node.get('level') == '1':
            level_1_term = " ".join(node.find('title').itertext())
            level_1_term_clean = inclusion_terms_clean(level_1_term)

            code_l1 = node.findtext('code')
            if node.findtext('code') is not None and node.findtext('code') not in [code_main]:
                output_list[i] = {'icd_code': code_l1,
                                  'term_list': [main, level_1_term],
                                  'level_0': main_clean,
                                  'level_1': level_1_term_clean}
                i += 1
        if node.get('level') == '2':
            level_2_term = " ".join(node.find('title').itertext())
            level_2_term_clean = inclusion_terms_clean(level_2_term)

            code_l2 = node.findtext('code')
            if node.findtext('code') is not None and node.findtext('code') not in [code_main, code_l1]:
                output_list[i] = {'icd_code': code_l2,
                                  'term_list': [main, level_1_term, level_2_term],
                                  'level_0': main_clean, 'level_1': level_1_term_clean, 'level_2': level_2_term_clean}
                i += 1
        if node.get('level') == '3':
            level_3_term = " ".join(node.find('title').itertext())
            level_3_term_clean = inclusion_terms_clean(level_3_term)

            code_l3 = node.findtext('code')
            if node.findtext('code') is not None and node.findtext('code') not in [code_main, code_l1, code_l2]:
                output_list[i] = {'icd_code': code_l3,
                                  'term_list': [main, level_1_term, level_2_term, level_3_term],
                                  'level_0': main_clean, 'level_1': level_1_term_clean, 'level_2': level_2_term_clean, 'level_3': level_3_term_clean}
                i += 1
        if node.get('level') == '4':
            level_4_term = " ".join(node.find('title').itertext())
            level_4_term_clean = inclusion_terms_clean(level_4_term)

            code_l4 = node.findtext('code')
            if node.findtext('code') is not None and node.findtext('code') not in [code_main, code_l1, code_l2, code_l3]:
                output_list[i] = {'icd_code': code_l4,
                                  'term_list':  [main, level_1_term, level_2_term, level_3_term, level_4_term],
                                  'level_0': main_clean, 'level_1': level_1_term_clean, 'level_2': level_2_term_clean,
                                  'level_3': level_3_term_clean, 'level_4': level_4_term_clean}
                i += 1
        if node.get('level') == '5':
            level_5_term = " ".join(node.find('title').itertext())
            level_5_term_clean = inclusion_terms_clean(level_5_term)

            code_l5 = node.findtext('code')
            if node.findtext('code') is not None and node.findtext('code') not in [code_main, code_l1, code_l2, code_l3, code_l4]:
                output_list[i] = {'icd_code': code_l5,
                                  'term_list': [main, level_1_term, level_2_term, level_3_term, level_4_term, level_5_term],
                                  'level_0': main_clean, 'level_1': level_1_term_clean, 'level_2': level_2_term_clean, 'level_3': level_3_term_clean,
                                  'level_4': level_4_term_clean, 'level_5': level_5_term_clean}
                i += 1
        if node.get('level') == '6':
            level_6_term = " ".join(node.find('title').itertext())
            level_6_term_clean = inclusion_terms_clean(level_6_term)

            code_l6 = node.findtext('code')
            if node.findtext('code') is not None and node.findtext('code') not in [code_main, code_l1, code_l2, code_l3, code_l4, code_l5]:
                output_list[i] = {'icd_code': code_l6,
                                  'term_list':  [main, level_1_term, level_2_term, level_3_term, level_4_term, level_5_term, level_6_term],
                                  'level_0': main_clean, 'level_1': level_1_term_clean, 'level_2': level_2_term_clean, 'level_3': level_3_term_clean,
                                  'level_4': level_4_term_clean, 'level_5': level_5_term_clean, 'level_6': level_6_term_clean}
                i += 1

        if node.get('level') == '7':
            level_7_term = " ".join(node.find('title').itertext())
            level_7_term_clean = inclusion_terms_clean(level_7_term)

            code_l7 = node.findtext('code')
            if node.findtext('code') is not None and node.findtext('code') not in [code_main, code_l1, code_l2, code_l3, code_l4, code_l5, code_l6]:
                output_list[i] = {'icd_code': code_l7,
                                  'term_list':  [main, level_1_term, level_2_term, level_3_term, level_4_term, level_5_term, level_6_term, level_7_term],
                                  'level_0': main_clean, 'level_1': level_1_term_clean, 'level_2': level_2_term_clean, 'level_3': level_3_term_clean,
                                  'level_4': level_4_term_clean, 'level_5': level_5_term_clean, 'level_6': level_6_term_clean, 'level_7': level_7_term_clean}
                i += 1

        if node.get('level') == '8':
            level_8_term = " ".join(node.find('title').itertext())
            level_8_term_clean = inclusion_terms_clean(level_8_term)

            code_l8 = node.findtext('code')
            if node.findtext('code') is not None and node.findtext('code') not in [code_main, code_l1, code_l2, code_l3, code_l4, code_l5, code_l6, code_l7]:
                output_list[i] = {'icd_code': code_l8,
                                  'term_list':  [main, level_1_term, level_2_term, level_3_term, level_4_term, level_5_term, level_6_term, level_7_term, level_8_term],
                                  'level_0': main_clean, 'level_1': level_1_term_clean, 'level_2': level_2_term_clean, 'level_3': level_3_term_clean,
                                  'level_4': level_4_term_clean, 'level_5': level_5_term_clean, 'level_6': level_6_term_clean, 'level_7': level_7_term_clean,
                                  'level_8': level_8_term_clean}
                i += 1

        if node.get('level') == '9':
            level_9_term = " ".join(node.find('title').itertext())
            level_9_term_clean = inclusion_terms_clean(level_9_term)

            code_l9 = node.findtext('code')
            if node.findtext('code') is not None and node.findtext('code') not in [code_main, code_l1, code_l2, code_l3, code_l4, code_l5, code_l6, code_l7, code_l8]:
                output_list[i] = {'icd_code': code_l9,
                                  'term_list': [main, level_1_term, level_2_term, level_3_term, level_4_term,
                                                level_5_term, level_6_term, level_7_term, level_8_term, level_9_term],
                                  'level_0': main_clean, 'level_1': level_1_term_clean, 'level_2': level_2_term_clean, 'level_3': level_3_term_clean,
                                  'level_4': level_4_term_clean, 'level_5': level_5_term_clean, 'level_6': level_6_term_clean, 'level_7': level_7_term_clean,
                                  'level_8': level_8_term_clean, 'level_9': level_9_term_clean}
                i += 1

    df_index = pd.DataFrame.from_dict(output_list, orient='index').reset_index()
    df_index['term_full'] = df_index.term_list.apply(lambda x: '; '.join(x))
    df_index.head()

    df_index['n_terms'] = 10 - df_index.isnull().sum(axis=1)
    df_index_long = pd.wide_to_long(df_index.drop(columns=['term_list']), stubnames='level_',
                                    i=['index', 'icd_code', 'n_terms'],
                                    j="level")
    df_index_long.reset_index(inplace=True)
    df_index_long.dropna(inplace=True)
    df_index_long.columns = ['seq_id', 'icd_codes', 'n_terms', 'level', 'term_full', 'terms']
    df_index_long['level'] = df_index_long['level']+1
    df_index_long.head()

    df_index_long['have_assci'] = df_index_long.terms.apply(is_ascii)
    df_index_long['terms'] = df_index_long.terms.str.replace(
        'é', 'e').str.replace('ö', 'o').str.replace('ë', 'e').str.replace('ç', 'c')
    df_index_long['terms'] = df_index_long.terms.str.replace(
        'ü', 'u').str.replace('à', 'a').str.replace('ä', 'a').str.replace('è', 'e')
    df_index_long['terms'] = df_index_long.terms.str.replace('Ö', 'o').str.replace('á', 'a').str.replace('ø', 'o')

    print("Loading keyword terms to dict")
    termDict = defaultdict(str)
    for index, row in df_index.iterrows():
        code = row[1].replace('.', '').replace('-', '')
        for term in row[2]:
            termDict[code] += term + ' '
    return termDict

# replace the non-ascii letter


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


# %%
#subset = df_index[['icd_code', 'term_list']]
#tuples = [tuple(x) for x in subset.values]
#tuplesLow = [(elem[0], [term.lower() for term in elem[1]]) for elem in tuples]
#
# %%
# for elem in tuplesLow:
#    for term in elem[1]:
#        if 'claudication' in term:
#            print(elem)
# %%
# for elem in tuplesLow:
#    for term in elem[1]:
#        if '\t' in term:
#            print(elem)
# %%
#maxTermLength = 0
#maxTermCount = 0
# for elem in tuplesLow:
#    for i, term in enumerate(elem[1]):
#        if i + 1 > maxTermCount:
#            maxTermCount = i + 1
#            print("LONGEST COUNT", elem, maxTermCount)
#        if len(term) > maxTermLength:
#            maxTermLength = len(term)
#            print("LONGEST TERM", term, maxTermLength)
#
# print(maxTermCount)
# print(maxTermLength)
