import pandas as pd, ast
from utils import *
from itertools import combinations

##---------------Step 1: Read excecl file----------------##

data_frame = pd.read_excel('Horizontal_Format.xlsx')


##---------------Step 2: Generate frequent itemsets and display support----------------##


support_count=int(input("Enter minimum support in percentage please: "))*len(data_frame.index)/100
min_confidence=float(input("Enter minimum confidence in percentage please: "))/100.0

baskets = list()

for row in data_frame.itertuples():
    baskets.append(pd.Series(str.split(row.items, ',')).drop_duplicates().tolist())

level1_candidates = list()
for basket in baskets:
    for item in basket:
        level1_candidates.append([item])
level1_candidates = sorted(pd.Series(level1_candidates).drop_duplicates().tolist())

frequent_itemsets = dict()
level1_frequent = dict()
for candidate in level1_candidates:
    level1_frequent[str(candidate)] = 0
 
for basket in baskets:
    for candidate in level1_candidates:
        if candidate[0] in basket:
            level1_frequent[str(candidate)]+=1

level1_frequent = {key: value for key, value in level1_frequent.items() if value >= support_count}

level = 1
print("\n" + "L" + str(level) + ": " + str(level1_frequent) + "\n")

frequent_itemsets.update(level1_frequent)

previous_level_based_candidates = [ast.literal_eval(item) for item in list(level1_frequent.keys())]

while(True):
    current_level_candidates = generate_candidates(previous_level_based_candidates)

    current_level_frequent = filter_frequent_itemsets(current_level_candidates, baskets, support_count)

    level+=1
    print("L" + str(level) + ": " + str(current_level_frequent) + "\n")

    frequent_itemsets.update(current_level_frequent)
    previous_level_based_candidates = [ast.literal_eval(item) for item in list(current_level_frequent.keys())]

    if len(previous_level_based_candidates) <= 1:
        
        print("\n" + "Frequent itemsets:" + str(frequent_itemsets) + "\n")
        print("Finished Generating Frequent Itemsets \n")
        break


##---------------Step 3: Represent frequent itemsets as asscocaition rules----------------##

all_rules = generate_all_rules(frequent_itemsets, len(data_frame.index))
print("\n" + "All Rules (X -> Y, Support, Confidence, Lift):")
for rule in all_rules:
    X, Y, support, confidence, lift = rule
    print(f"{X} -> {Y} (Support: {support}, Confidence: {confidence:.2f}, Lift: {lift:.2f})")


##------------------Step 4: Filter strong rules-------------------##

strong_rules = [item for item in all_rules if item[3]>=min_confidence]
print("\n" + "Strong Rules (X -> Y, Support, Confidence, Lift):")
for rule in strong_rules:
    X, Y, support, confidence, lift = rule
    print(f"{X} -> {Y} (Support: {support}, Confidence: {confidence:.2f}, Lift: {lift:.2f})")


##---------------Step 5: Visualize frequent itemsets----------------##

visualize_frequent_itemsets(frequent_itemsets)
