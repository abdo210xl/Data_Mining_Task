import pandas as pd, ast
from utils import *
from itertools import combinations

def generate_strong_rules(frequent_itemsets, baskets, min_confidence):
    """
    Generate strong association rules from frequent itemsets.

    Args:
    - frequent_itemsets: List of dictionaries with frequent itemsets and their support counts.
    - baskets: List of transactions.
    - min_confidence: Minimum confidence threshold.

    Returns:
    - rules: List of tuples (X, Y, support, confidence, lift, strong).
    """
    rules = []    
    # Helper function to calculate support
    def calculate_support(itemset):
        itemset = set(itemset)
        count = sum(1 for basket in baskets if itemset.issubset(basket))
        
        return count

    # Loop through all levels of frequent itemsets
    for level in frequent_itemsets[1:]:  # Skip level 0 (single items don't generate rules)
        for itemset, support_count in level.items():
            itemset = ast.literal_eval(itemset)  # Convert string representation to list
            itemset_support = support_count   # Support of the full itemset
            
            # Generate all possible subsets (X) and Y = itemset - X
            for i in range(1, len(itemset)):
                subsets = combinations(itemset, i)
                for subset in subsets:
                    X = set(subset)
                    Y = set(itemset) - X

                    # Calculate confidence
                    X_support = calculate_support(X)

                    if X_support > 0: 
                        confidence = itemset_support / X_support
                        Y_support = calculate_support(Y)
                        # print(X)
                        # print(X_support) 
                        # print("\n")
                        # print(Y)
                        # print(Y_support)  
                          
                        # Calculate lift
                        lift = confidence / Y_support if Y_support > 0 else 0
                        
                        # Check if the rule is strong based on min_confidence
                        is_strong = confidence >= min_confidence
                        
                        if is_strong :
                            # Store the rule with all relevant details
                            rules.append((list(X), list(Y), itemset_support, confidence, lift))
    
    return rules


data_frame = pd.read_excel('Horizontal_Format.xlsx')
SUPPORT_COUNT=3

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

level1_frequent = {key: value for key, value in level1_frequent.items() if value >= SUPPORT_COUNT}

frequent_itemsets.append(level1_frequent)

previous_level_based_candidates = [ast.literal_eval(item) for item in list(level1_frequent.keys())]

print(previous_level_based_candidates)
print( "\n")


while(True):
    current_level_candidates = generate_candidates(previous_level_based_candidates)
    print(current_level_candidates)
    print( "\n")

    current_level_frequent = filter_frequent_itemsets(current_level_candidates, baskets, SUPPORT_COUNT)
    print(current_level_frequent)
    print( "\n")

    frequent_itemsets.append(current_level_frequent)
    previous_level_based_candidates = [ast.literal_eval(item) for item in list(current_level_frequent.keys())]
    print(previous_level_based_candidates)
    print( "\n")

    if len(previous_level_based_candidates) <= 1:
        print("finished apreori")
        print( "\n")
        print(frequent_itemsets)
        print( "\n")

        break

strong_rules = generate_strong_rules(frequent_itemsets, baskets, 0.5)

# Display the rules with all relevant details
print("Strong Rules (X -> Y, Support, Confidence, Lift):")
for rule in strong_rules:
    X, Y, support, confidence, lift = rule
    print(f"{X} -> {Y} (Support: {support}, Confidence: {confidence:.2f}, Lift: {lift:.2f})")
