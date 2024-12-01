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

print(baskets)
print( "\n")

level1_candidates = list()
for basket in baskets:
    for item in basket:
        level1_candidates.append([item])
level1_candidates = sorted(pd.Series(level1_candidates).drop_duplicates().tolist())

print(level1_candidates)
print( "\n")


frequent_itemsets = list()
level1_frequent = dict()
for candidate in level1_candidates:
    level1_frequent[str(candidate)] = 0
 
for basket in baskets:
    for candidate in level1_candidates:
        if candidate[0] in basket:
            level1_frequent[str(candidate)]+=1

level1_frequent = {key: value for key, value in level1_frequent.items() if value >= support_count}

frequent_itemsets.append(level1_frequent)

previous_level_based_candidates = [ast.literal_eval(item) for item in list(level1_frequent.keys())]

level = 1
print("L"+str(level)+": ")
print(previous_level_based_candidates)
print( "\n")
level+=1

while(True):
    current_level_candidates = generate_candidates(previous_level_based_candidates)
    # print(current_level_candidates)
    # print( "\n")

    current_level_frequent = filter_frequent_itemsets(current_level_candidates, baskets, support_count)
    print("L"+str(level)+": ")
    print(current_level_frequent)
    print( "\n")

    frequent_itemsets.append(current_level_frequent)
    previous_level_based_candidates = [ast.literal_eval(item) for item in list(current_level_frequent.keys())]
    # print(previous_level_based_candidates)
    # print( "\n")

    if len(previous_level_based_candidates) <= 1:
        
        print( "Frequent itemsets:")
        print(frequent_itemsets)
        print("Finished apriori")
        print("\n")

        break
    level+=1

##---------------Step 3: Visualize frequent itemsets----------------##

visualize_frequent_itemsets(frequent_itemsets)


##---------------Step 4: Represent frequent itemsets as asscocaition rules----------------##

strong_rules = generate_strong_rules(frequent_itemsets, baskets, min_confidence)


##---------------Step 5 and 6: Generate strong rules, calculate lift----------------##

print("Strong Rules (X -> Y, Support, Confidence, Lift):")
for rule in strong_rules:
    X, Y, support, confidence, lift = rule
    print(f"{X} -> {Y} (Support: {support}, Confidence: {confidence:.2f}, Lift: {lift:.2f})")



