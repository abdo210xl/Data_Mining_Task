import pandas as pd, ast
from utils import *

data_frame = pd.read_excel('Horizontal_Format.xlsx')
SUPPORT_COUNT=3

baskets = list()

for row in data_frame.itertuples():
    baskets.append(pd.Series(str.split(row.items, ',')).drop_duplicates().tolist())

print(baskets)

level1_candidates = list()
for basket in baskets:
    for item in basket:
        level1_candidates.append([item])
level1_candidates = sorted(pd.Series(level1_candidates).drop_duplicates().tolist())

print(level1_candidates)

frequent_itemsets = list()
level1_frequent = dict()
for candidate in level1_candidates:
    level1_frequent[str(candidate)] = 0
 
for basket in baskets:
    for candidate in level1_candidates:
        if candidate[0] in basket:
            level1_frequent[str(candidate)]+=1

level1_frequent = {key: value for key, value in level1_frequent.items() if value >= SUPPORT_COUNT}

frequent_itemsets.append(level1_frequent)

previous_level_based_candidates = [ast.literal_eval(item) for item in list(level1_frequent.keys())]

print(previous_level_based_candidates)

while(True):
    current_level_candidates = generate_candidates(previous_level_based_candidates)
    print(current_level_candidates)
    current_level_frequent = filter_frequent_itemsets(current_level_candidates, baskets, SUPPORT_COUNT)
    print(current_level_frequent)
    frequent_itemsets.append(current_level_frequent)
    previous_level_based_candidates = [ast.literal_eval(item) for item in list(current_level_frequent.keys())]
    print(previous_level_based_candidates)
    if len(previous_level_based_candidates) <= 1:
        print("finished apreori")
        print(frequent_itemsets)
        break
