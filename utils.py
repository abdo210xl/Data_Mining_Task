import matplotlib.pyplot as plt, ast
from itertools import combinations


def generate_candidates(past_level_candidates):
    generated_itemets = list()
    other_candidates = past_level_candidates.copy()
    for candidate in past_level_candidates:
        prefix_removed = candidate.copy()
        prefix_removed.pop(0)
        other_candidates.pop(0)
        for other_candidate in other_candidates:
            postfix_removed = other_candidate.copy()
            postfix_removed.pop()
            if prefix_removed == postfix_removed:
                new_candidate = postfix_removed
                new_candidate.insert(0, candidate[0])
                new_candidate.append(other_candidate[-1])
                generated_itemets.append(new_candidate)
    return generated_itemets

def filter_frequent_itemsets(candidates, baskets, support_count):
    itemsets = dict()
    for candidate in candidates:
        itemsets[str(candidate)] = 0
    is_in_basket = True
    for candidate in candidates:
        for basket in baskets:
            for item in candidate:
                if item not in basket:
                    is_in_basket = False
                    break
            if is_in_basket:
                itemsets[str(candidate)] += 1
            is_in_basket = True
    # print(itemsets)
    frequent_itemsets =  {key: value for key, value in itemsets.items() if value >= support_count}
    return frequent_itemsets

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


def visualize_frequent_itemsets(frequent_itemsets):
    visual_frequent_itemsets = dict()
    for level in frequent_itemsets:
        visual_frequent_itemsets.update(level)
    #print(visual_frequent_itemsets)

    x_labels = list(visual_frequent_itemsets.keys())
    y_values = list(visual_frequent_itemsets.values())

    plt.figure(figsize=(12, 5))

    plt.bar(x_labels, y_values, color='skyblue')

    plt.xlabel("Frequent Itemsets")
    plt.ylabel("Support")
    plt.title("Frequent Itesets Bar Chart")

    plt.show()

